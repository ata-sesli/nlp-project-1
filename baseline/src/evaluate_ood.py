
"""Evaluate saved TF-IDF baselines on OOD datasets."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "LucidAI-Dataset" / "data"
MODELS = ROOT / "models"
RESULTS = ROOT / "results"

OOD_FILES = [
    "ood_approve_or_deny.csv.gz",
    "ood_saroku.csv.gz",
]


def evaluate(y_true, y_pred):
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "deny_precision": float(
            precision_score(y_true, y_pred, pos_label=1, zero_division=0)
        ),
        "deny_recall": float(
            recall_score(y_true, y_pred, pos_label=1, zero_division=0)
        ),
        "deny_f1": float(
            f1_score(y_true, y_pred, pos_label=1, zero_division=0)
        ),
        "confusion_matrix": confusion_matrix(
            y_true, y_pred, labels=[0, 1]
        ).tolist(),
    }


def main():
    all_results = {}

    for input_name in ("input_a", "input_b"):
        model_path = MODELS / f"tfidf_logreg_{input_name}.joblib"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        model = joblib.load(model_path)
        all_results[input_name] = {}

        for filename in OOD_FILES:
            data_path = DATA / filename
            df = pd.read_csv(data_path)

            y_true = df["label"].astype(int)
            X = df[input_name].fillna("").astype(str)

            print(f"\nDataset: {filename} | Input: {input_name}")
            print(f"Rows: {len(df):,}")

            predictions = model.predict(X)
            metrics = evaluate(y_true, predictions)

            all_results[input_name][filename] = {
                "rows": len(df),
                **metrics,
            }

            print(json.dumps(metrics, indent=2))

    RESULTS.mkdir(exist_ok=True)
    output_path = RESULTS / "ood_baselines.json"
    output_path.write_text(
        json.dumps(
            {
                "label_mapping": {"0": "allow", "1": "deny"},
                "results": all_results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
