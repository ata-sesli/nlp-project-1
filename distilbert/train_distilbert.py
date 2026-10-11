"""Fine-tune DistilBERT to decide whether an agent tool call should be allowed (0) or denied (1).

Example (Colab, free T4):
    python train_distilbert.py --data-dir LucidAI-Dataset/data --input a --out runs/distilbert_a
    python train_distilbert.py --data-dir LucidAI-Dataset/data --input b --out runs/distilbert_b

Outputs in --out:
    model/                  fine-tuned weights + tokenizer (load with AutoModelForSequenceClassification)
    predictions/<split>.csv id, label, p_deny for every row of every predicted split
    run.json                all settings, data sizes, training time and inference speed
"""

import argparse
import glob
import json
import os
import random
import time

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, Trainer,
                          TrainingArguments, set_seed)
from transformers.trainer_utils import get_last_checkpoint

DEFAULTS = {  # per input format: (train rows, max tokens, batch size)
    "a": (100_000, 128, 64),
    "b": (60_000, 512, 16),
}
META = ["id", "label", "length_bucket", "difficulty"]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data-dir", default="LucidAI-Dataset/data")
    p.add_argument("--input", choices=["a", "b"], required=True, help="a = tool call only, b = call + request + history")
    p.add_argument("--model", default="distilbert-base-uncased")
    p.add_argument("--out", required=True, help="output folder; put it on Google Drive to survive disconnects")
    p.add_argument("--train-rows", type=int, help="stratified subsample of train (0 = all rows)")
    p.add_argument("--val-rows", type=int, default=5_000, help="val rows used for evaluation during training")
    p.add_argument("--max-len", type=int)
    p.add_argument("--batch-size", type=int)
    p.add_argument("--epochs", type=float, default=1.0)
    p.add_argument("--lr", type=float, default=3e-5)
    p.add_argument("--eval-every", type=int, default=500, help="steps between evaluations and checkpoints")
    p.add_argument("--predict", default="val,test,ood_approve_or_deny,ood_saroku",
                   help="splits to write predictions for (comma separated, empty = none)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--smoke", action="store_true", help="tiny run to check that everything works")
    a = p.parse_args()
    rows, max_len, batch = DEFAULTS[a.input]
    a.train_rows = rows if a.train_rows is None else a.train_rows
    a.max_len = a.max_len or max_len
    a.batch_size = a.batch_size or batch
    if a.smoke:
        a.train_rows, a.val_rows, a.eval_every = 256, 64, 4
    return a


def load_split(data_dir, name, text_col, limit=None):
    files = sorted(glob.glob(os.path.join(data_dir, f"{name}*.csv.gz")))
    if not files:
        raise FileNotFoundError(f"no files for split '{name}' in {data_dir}")
    # engine="python": a few rows contain NUL characters that the C reader cuts off
    df = pd.concat([pd.read_csv(f, engine="python", usecols=META + [text_col]) for f in files],
                   ignore_index=True)
    df = df.rename(columns={text_col: "text"})
    df["text"] = df["text"].fillna("").astype(str)
    return df.head(limit) if limit else df


def stratified_sample(df, n, seed):
    """Keep the label / length / difficulty mix of the full split."""
    if not n or n >= len(df):
        return df.sample(frac=1, random_state=seed).reset_index(drop=True)
    strata = df["label"].astype(str) + "|" + df["length_bucket"].astype(str) + "|" + df["difficulty"].astype(str)
    frac = n / len(df)
    parts = [g.sample(n=max(1, round(len(g) * frac)), random_state=seed) for _, g in df.groupby(strata)]
    return pd.concat(parts).sample(frac=1, random_state=seed).reset_index(drop=True)


class TextDataset(Dataset):
    def __init__(self, df):
        self.text, self.label = df["text"].tolist(), df["label"].astype(int).tolist()

    def __len__(self):
        return len(self.text)

    def __getitem__(self, i):
        return {"text": self.text[i], "label": self.label[i]}


class Collator:
    """Tokenizes per batch, so padding is only as long as the longest text in the batch.
    Truncation cuts the END of the text. The call and the user request come first in the
    input, so a cut only loses the last agent-history steps."""

    def __init__(self, tokenizer, max_len):
        self.tok, self.max_len = tokenizer, max_len

    def __call__(self, batch):
        enc = self.tok([b["text"] for b in batch], truncation=True, max_length=self.max_len,
                       padding=True, return_tensors="pt")
        enc["labels"] = torch.tensor([b["label"] for b in batch])
        return enc


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    pred = logits.argmax(-1)
    tp = int(((pred == 1) & (labels == 1)).sum())
    fp = int(((pred == 1) & (labels == 0)).sum())
    fn = int(((pred == 0) & (labels == 1)).sum())
    tn = int(((pred == 0) & (labels == 0)).sum())
    f1_deny = 2 * tp / max(1, 2 * tp + fp + fn)
    f1_allow = 2 * tn / max(1, 2 * tn + fn + fp)
    return {"accuracy": (tp + tn) / len(labels), "macro_f1": (f1_deny + f1_allow) / 2,
            "false_allow_rate": fn / max(1, tp + fn)}


@torch.no_grad()
def predict(model, tok, df, max_len, batch_size, device):
    """Returns P(deny) for every row, in the original row order."""
    model.eval()
    order = np.argsort(df["text"].str.len().to_numpy())  # similar lengths together = less padding
    texts = df["text"].to_numpy()[order]
    probs = np.empty(len(df), dtype=np.float32)
    use_amp = device == "cuda"
    start = time.time()
    for i in range(0, len(texts), batch_size):
        enc = tok(list(texts[i:i + batch_size]), truncation=True, max_length=max_len,
                  padding=True, return_tensors="pt").to(device)
        with torch.autocast(device_type=device, dtype=torch.float16, enabled=use_amp):
            logits = model(**enc).logits.float()
        probs[i:i + batch_size] = torch.softmax(logits, -1)[:, 1].cpu().numpy()
    seconds = time.time() - start
    out = np.empty_like(probs)
    out[order] = probs
    return out, seconds


def main():
    a = parse_args()
    set_seed(a.seed)
    random.seed(a.seed)
    os.makedirs(a.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    text_col = f"input_{a.input}"
    print(f"device={device}  input={text_col}  model={a.model}")

    t0 = time.time()
    train = stratified_sample(load_split(a.data_dir, "train", text_col), a.train_rows, a.seed)
    val_full = load_split(a.data_dir, "val", text_col)
    val_small = stratified_sample(val_full, a.val_rows, a.seed)
    print(f"train rows={len(train)}  val rows (during training)={len(val_small)}  "
          f"deny share={train['label'].mean():.3f}  load {time.time() - t0:.0f}s")

    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForSequenceClassification.from_pretrained(
        a.model, num_labels=2, id2label={0: "allow", 1: "deny"}, label2id={"allow": 0, "deny": 1})

    ckpt_dir = os.path.join(a.out, "checkpoints")
    total_steps = int(np.ceil(len(train) / a.batch_size) * a.epochs)
    args = TrainingArguments(
        output_dir=ckpt_dir,
        num_train_epochs=a.epochs,
        learning_rate=a.lr,
        warmup_steps=int(0.06 * total_steps),  # 6% linear warm-up
        weight_decay=0.01,
        per_device_train_batch_size=a.batch_size,
        per_device_eval_batch_size=a.batch_size * 2,
        fp16=device == "cuda",
        eval_strategy="steps",
        eval_steps=a.eval_every,
        save_strategy="steps",
        save_steps=a.eval_every,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        logging_steps=50,
        report_to="none",
        remove_unused_columns=False,
        dataloader_num_workers=2,
        seed=a.seed,
        use_cpu=device == "cpu",
    )
    trainer = Trainer(model=model, args=args, train_dataset=TextDataset(train),
                      eval_dataset=TextDataset(val_small), data_collator=Collator(tok, a.max_len),
                      compute_metrics=compute_metrics)

    last = get_last_checkpoint(ckpt_dir) if os.path.isdir(ckpt_dir) else None
    if last:
        print(f"resuming from {last}")
    t0 = time.time()
    trainer.train(resume_from_checkpoint=last)
    train_seconds = time.time() - t0
    best_eval = trainer.evaluate()
    print("best checkpoint on val sample:", best_eval)

    model_dir = os.path.join(a.out, "model")
    trainer.save_model(model_dir)
    tok.save_pretrained(model_dir)

    run = {"settings": vars(a), "device": device,
           "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
           "train_rows": len(train), "train_seconds": round(train_seconds, 1),
           "val_sample_metrics": best_eval, "predictions": {}}

    pred_dir = os.path.join(a.out, "predictions")
    os.makedirs(pred_dir, exist_ok=True)
    model = trainer.model.to(device)
    for split in [s for s in a.predict.split(",") if s]:
        df = val_full if split == "val" else load_split(a.data_dir, split, text_col)
        if a.smoke:
            df = df.sample(n=min(64, len(df)), random_state=a.seed)
        p_deny, seconds = predict(model, tok, df, a.max_len, a.batch_size * 2, device)
        pd.DataFrame({"id": df["id"], "label": df["label"], "p_deny": p_deny}).to_csv(
            os.path.join(pred_dir, f"{split}.csv"), index=False)
        acc = float(((p_deny >= 0.5).astype(int) == df["label"].to_numpy()).mean())
        run["predictions"][split] = {"rows": len(df), "seconds": round(seconds, 1),
                                     "rows_per_second": round(len(df) / max(seconds, 1e-9), 1),
                                     "accuracy_at_0.5": round(acc, 4)}
        print(f"{split}: {len(df)} rows  acc@0.5={acc:.4f}  {seconds:.0f}s")

    with open(os.path.join(a.out, "run.json"), "w") as f:
        json.dump(run, f, indent=2, default=str)
    print(f"done -> {a.out}")


if __name__ == "__main__":
    main()
