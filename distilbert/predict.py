"""Score agent tool calls with a fine-tuned DistilBERT: P(deny) and an allow/deny decision.

The model is loaded from the Hugging Face Hub (or a local folder) and cached, so only the
first run downloads it.

One input, text from stdin (the MayI input format: tool call, user request, agent history):
    echo "### PROPOSED TOOL CALL ..." | python predict.py --text -

A whole CSV (e.g. the dataset's test split), predictions written to a new CSV:
    python predict.py --input data/test.csv.gz --text-col input_b --out predictions/test.csv

Model: --model, else the MODEL_ID environment variable.
"""

import argparse
import os
import sys
import time

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", default=os.environ.get("MODEL_ID"),
                   help="Hub id (user/name) or local folder; default: $MODEL_ID")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="one input text, or '-' to read it from stdin")
    src.add_argument("--input", help="CSV / CSV.GZ file with one text per row")
    p.add_argument("--text-col", default="input_b", help="column holding the text in --input")
    p.add_argument("--out", help="CSV to write predictions to (with --input)")
    p.add_argument("--threshold", type=float, default=0.5, help="deny when p_deny >= threshold")
    p.add_argument("--max-len", type=int, default=512)
    p.add_argument("--batch-size", type=int, default=32)
    a = p.parse_args()
    if not a.model:
        p.error("no model: pass --model or set MODEL_ID")
    if a.input and not a.out:
        p.error("--input needs --out")
    return a


@torch.no_grad()
def score(model, tok, texts, max_len, batch_size, device):
    """P(deny) for each text, in input order. Similar lengths are batched together to cut padding."""
    order = np.argsort([len(t) for t in texts])
    probs = np.empty(len(texts), dtype=np.float32)
    for i in range(0, len(texts), batch_size):
        idx = order[i:i + batch_size]
        enc = tok([texts[j] for j in idx], truncation=True, max_length=max_len,
                  padding=True, return_tensors="pt").to(device)
        probs[idx] = torch.softmax(model(**enc).logits.float(), -1)[:, 1].cpu().numpy()
    return probs


def main():
    a = parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForSequenceClassification.from_pretrained(a.model).to(device).eval()
    print(f"model={a.model} device={device} loaded in {time.time() - t0:.1f}s", file=sys.stderr)

    if a.text is not None:
        text = sys.stdin.read() if a.text == "-" else a.text
        p = float(score(model, tok, [text], a.max_len, 1, device)[0])
        print(f"p_deny={p:.4f} decision={'deny' if p >= a.threshold else 'allow'}")
        return

    # engine="python": some rows contain NUL characters that the C reader cuts off
    df = pd.read_csv(a.input, engine="python")
    texts = df[a.text_col].fillna("").astype(str).tolist()
    t0 = time.time()
    p = score(model, tok, texts, a.max_len, a.batch_size, device)
    seconds = time.time() - t0
    out = pd.DataFrame({"id": df["id"] if "id" in df else range(len(df)), "p_deny": p})
    if "label" in df:
        out.insert(1, "label", df["label"])
        print(f"accuracy@{a.threshold}: {((p >= a.threshold).astype(int) == df['label']).mean():.4f}", file=sys.stderr)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    out.to_csv(a.out, index=False)
    print(f"{len(df)} rows in {seconds:.1f}s ({len(df) / max(seconds, 1e-9):.1f} rows/s) -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
