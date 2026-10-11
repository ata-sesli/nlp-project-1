"""Score the BiLSTM models (A and B) for the benchmark.

Loads bilstm/results/models/{a,b}/bilstm_{A,B}.pt. Each file holds the trained weights and the
vocabulary, so nothing is retrained. The model and the tokenizer below are the ones from
bilstm/notebooks/BILSTM.ipynb. Scoring uses a GPU when there is one; latency is always measured
on the CPU, one row per call.

    python benchmark/score_bilstm.py
    python benchmark/score_bilstm.py --limit 1000   # the same fixed sample as the other scorers
"""

import argparse
import os
import re

import numpy as np
import torch
import torch.nn as nn

from common import MODELS, ROOT, SPLITS, load_texts, measure_latency, write_predictions

MAX_LEN, EMBEDDING_DIM, HIDDEN_DIM = 128, 100, 128


class BiLSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, bidirectional=True,
                            num_layers=2, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(self.embedding(x))
        pooled, _ = torch.max(lstm_out, dim=1)
        return self.fc(self.dropout(pooled)).squeeze(1)


def encode(texts, vocab):
    """Token ids, cut or padded to MAX_LEN; unknown words map to <UNK>."""
    rows = []
    for text in texts:
        ids = [vocab.get(t, vocab["<UNK>"]) for t in re.findall(r"\b\w+\b|\[SEP\]", str(text).lower())[:MAX_LEN]]
        rows.append(ids + [vocab["<PAD>"]] * (MAX_LEN - len(ids)))
    return torch.tensor(rows, dtype=torch.long)


@torch.no_grad()
def score(model, vocab, texts, batch_size, device):
    probs = []
    for i in range(0, len(texts), batch_size):
        x = encode(texts[i:i + batch_size], vocab).to(device)
        probs.append(torch.sigmoid(model(x)).cpu().numpy())
    return np.concatenate(probs)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--splits", default=",".join(SPLITS))
    ap.add_argument("--limit", type=int, default=0, help="score a fixed random sample of this many rows per split")
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--no-latency", action="store_true")
    a = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    for name in ("bilstm_a", "bilstm_b"):
        col = MODELS[name][2]
        letter = col[-1]
        path = os.path.join(ROOT, "bilstm", "results", "models", letter, f"bilstm_{letter.upper()}.pt")
        checkpoint = torch.load(path, map_location="cpu", weights_only=True)
        vocab = checkpoint["vocab"]
        model = BiLSTMClassifier(len(vocab), EMBEDDING_DIM, HIDDEN_DIM)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.to(device).eval()
        for split in filter(None, a.splits.split(",")):
            df = load_texts(split, col, limit=a.limit)
            write_predictions(name, split, df, score(model, vocab, df[col].tolist(), a.batch_size, device))
        if not a.no_latency:
            model.to("cpu")
            measure_latency(name, lambda t: score(model, vocab, [t], 1, "cpu"), col)


if __name__ == "__main__":
    main()
