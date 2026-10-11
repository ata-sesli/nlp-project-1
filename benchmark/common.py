"""Shared pieces of the benchmark: the model list, data loading and the predictions format.

Every scorer writes, per model:
    predictions/<model>/<split>.csv   id, label, p_deny
    predictions/<model>/latency.json  CPU time per row, one row at a time
run_benchmark.py reads only these files, so a new model needs only a new scorer.
"""

import glob
import json
import os
import platform
import time

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "dataset", "data")
PRED = os.path.join(ROOT, "benchmark", "predictions")
SPLITS = ["test", "ood_approve_or_deny", "ood_saroku"]

# name: (architecture, specific model, input column, role)
MODELS = {
    "tfidf_logreg_a": ("TF-IDF + Logistic Regression", "word 1-2 grams, 100k features", "input_a", "baseline"),
    "tfidf_logreg_b": ("TF-IDF + Logistic Regression", "word 1-2 grams, 100k features", "input_b", "baseline"),
    "distilbert_a": ("DistilBERT", "distilbert-base-uncased, fine-tuned", "input_a", "baseline"),
    "distilbert_b": ("DistilBERT", "distilbert-base-uncased, fine-tuned", "input_b", "baseline"),
}


def model_info(name):
    """Registry entry for a model; a model that is not registered is described by its folder name."""
    if name in MODELS:
        return MODELS[name]
    return (name, name, "input_a" if name.endswith("_a") else "input_b", "baseline")


def load_split(split, cols):
    files = sorted(glob.glob(os.path.join(DATA, f"{split}*.csv.gz")))
    if not files:
        raise FileNotFoundError(f"no files for split {split} in {DATA}")
    # engine="python": some rows contain NUL characters that the C reader cuts off
    return pd.concat([pd.read_csv(f, engine="python", usecols=cols) for f in files], ignore_index=True)


def load_texts(split, col, limit=0, seed=42):
    """id, label and one text column of a split; limit > 0 takes a fixed random sample."""
    df = load_split(split, ["id", "label", col])
    if limit and limit < len(df):
        df = df.sample(n=limit, random_state=seed).reset_index(drop=True)
    df[col] = df[col].fillna("").astype(str)
    return df


def write_predictions(model, split, df, p_deny):
    out = os.path.join(PRED, model)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"{split}.csv")
    pd.DataFrame({"id": df["id"], "label": df["label"].astype(int), "p_deny": p_deny}).to_csv(path, index=False)
    acc = ((np.asarray(p_deny) >= 0.5).astype(int) == df["label"].to_numpy()).mean()
    print(f"{model} {split}: {len(df)} rows, accuracy@0.5={acc:.4f} -> {path}")


def measure_latency(model, predict_one, col, rows=200, warmup=5, seed=42):
    """Times predict_one(text) on a fixed sample of test rows, one row per call, and writes latency.json."""
    texts = load_texts("test", col, limit=rows, seed=seed)[col].tolist()
    for t in texts[:warmup]:
        predict_one(t)
    ms = []
    for t in texts:
        t0 = time.perf_counter()
        predict_one(t)
        ms.append((time.perf_counter() - t0) * 1000)
    report = {"rows": len(ms), "ms_mean": float(np.mean(ms)), "ms_p50": float(np.percentile(ms, 50)),
              "ms_p95": float(np.percentile(ms, 95)), "device": "cpu", "batch_size": 1,
              "machine": f"{platform.system()} {platform.machine()}", "cpu_count": os.cpu_count()}
    out = os.path.join(PRED, model)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "latency.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(f"{model} latency: p50={report['ms_p50']:.2f} ms, p95={report['ms_p95']:.2f} ms per row (CPU)")
