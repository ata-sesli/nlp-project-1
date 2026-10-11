"""Score the TF-IDF + Logistic Regression baselines (A and B) for the benchmark.

Loads baseline/models/tfidf_logreg_input_{a,b}.joblib. The model files are not in the repo;
train them first:
    python baseline/src/baseline.py --input input_a
    python baseline/src/baseline.py --input input_b

Then:
    python benchmark/score_baseline.py
    python benchmark/score_baseline.py --limit 1000   # the same fixed sample as the other scorers
"""

import argparse
import os
import sys

import joblib

from common import MODELS, ROOT, SPLITS, load_texts, measure_latency, write_predictions


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--splits", default=",".join(SPLITS))
    ap.add_argument("--limit", type=int, default=0, help="score a fixed random sample of this many rows per split")
    ap.add_argument("--no-latency", action="store_true")
    a = ap.parse_args()

    for name in ("tfidf_logreg_a", "tfidf_logreg_b"):
        col = MODELS[name][2]
        path = os.path.join(ROOT, "baseline", "models", f"tfidf_logreg_{col}.joblib")
        if not os.path.exists(path):
            sys.exit(f"missing {path}: run  python baseline/src/baseline.py --input {col}")
        model = joblib.load(path)
        for split in filter(None, a.splits.split(",")):
            df = load_texts(split, col, limit=a.limit)
            write_predictions(name, split, df, model.predict_proba(df[col])[:, 1])
        if not a.no_latency:
            measure_latency(name, lambda t: model.predict_proba([t]), col)


if __name__ == "__main__":
    main()
