
"""Evaluate saved TF-IDF baselines on the untouched test split."""

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
    test_path = DATA / "test.csv.gz"
    test = pd.read_csv(test_path)
    y_test = test["label"].astype(int)

    print(f"Test rows: {len(test):,}")
    all_results = {}

    RESULTS.mkdir(exist_ok=True)

    for input_name in ("input_a", "input_b"):
        model_path = MODELS / f"tfidf_logreg_{input_name}.joblib"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        model = joblib.load(model_path)
        X_test = test[input_name].fillna("").astype(str)

        print(f"Evaluating {input_name}...")

        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        metrics = evaluate(y_test, predictions)
        all_results[input_name] = metrics

        prediction_path = RESULTS / f"pred_test_{input_name}.csv"
        pd.DataFrame({
            "id": test["id"],
            "label": y_test,
            "prediction": predictions,
            "p_deny": probabilities,
        }).to_csv(prediction_path, index=False)

        print(json.dumps({input_name: metrics}, indent=2))
        print(f"Predictions saved to: {prediction_path}")

    output_path = RESULTS / "test_baselines.json"
    output_path.write_text(
        json.dumps(
            {
                "dataset": "LucidAI-Dataset/test.csv.gz",
                "test_rows": len(test),
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
