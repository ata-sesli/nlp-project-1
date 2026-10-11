"""Score the fine-tuned DistilBERT models (A and B) for the benchmark.

The models are downloaded from the Hugging Face Hub on the first run. Scoring uses a GPU when
there is one; latency is always measured on the CPU, one row per call.

Everything (a GPU is recommended: B scores about 8 rows/s on a laptop CPU):
    python benchmark/score_distilbert.py

On a CPU, a fixed sample of each split and the latency:
    python benchmark/score_distilbert.py --limit 2000

Latency only (the predictions come from somewhere else, e.g. the training run):
    python benchmark/score_distilbert.py --splits ""
"""

import argparse
import os
import sys

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from common import MODELS, ROOT, SPLITS, load_texts, measure_latency, write_predictions

sys.path.insert(0, os.path.join(ROOT, "distilbert"))
from predict import score  # noqa: E402  (same scoring code as distilbert/predict.py)

HUB = {  # name: (Hub id, max tokens used in training)
    "distilbert_a": ("akifkulll/mayi-distilbert-a", 128),
    "distilbert_b": ("akifkulll/mayi-distilbert-b", 512),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", default=",".join(HUB))
    ap.add_argument("--splits", default=",".join(SPLITS))
    ap.add_argument("--limit", type=int, default=0, help="score a fixed random sample of this many rows per split")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--no-latency", action="store_true")
    a = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    for name in filter(None, a.models.split(",")):
        hub_id, max_len = HUB[name]
        col = MODELS[name][2]
        tok = AutoTokenizer.from_pretrained(hub_id)
        model = AutoModelForSequenceClassification.from_pretrained(hub_id).to(device).eval()
        for split in filter(None, a.splits.split(",")):
            df = load_texts(split, col, limit=a.limit)
            write_predictions(name, split, df, score(model, tok, df[col].tolist(), max_len, a.batch_size, device))
        if not a.no_latency:
            model.to("cpu")
            measure_latency(name, lambda t: score(model, tok, [t], max_len, 1, "cpu"), col)


if __name__ == "__main__":
    main()
