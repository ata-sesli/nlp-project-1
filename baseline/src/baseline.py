"""TF-IDF + Logistic Regression baseline for the dataset in dataset/data."""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
import numpy as np
import numpy as np
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT.parent / "dataset" / "data"
MODELS = ROOT / "models"
RESULTS = ROOT / "results"


def load_split(name):
    files = sorted(DATA.glob(f"{name}*.csv.gz"))
    if not files:
        raise FileNotFoundError(f"No files found for split: {name}")

    frames = [pd.read_csv(path) for path in files]
    return pd.concat(frames, ignore_index=True)


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        choices=["input_a", "input_b"],
        required=True,
        help="Use command-only input_a or contextual input_b",
    )
    args = parser.parse_args()

    MODELS.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)

    print("Loading training data...")
    train = load_split("train")
    print(f"Training rows: {len(train):,}")

    print("Loading validation data...")
    val = load_split("val")
    print(f"Validation rows: {len(val):,}")

    # Only the selected text field is used. Rationale/category are excluded.
    X_train = train[args.input].fillna("").astype(str)
    y_train = train["label"].astype(int)
    X_val = val[args.input].fillna("").astype(str)
    y_val = val["label"].astype(int)

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                strip_accents="unicode",
                ngram_range=(1, 2),
                min_df=2,
                max_features=100_000,
                sublinear_tf=True,
                dtype=np.float32,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=200,
                solver="liblinear",
                random_state=42,
            ),
        ),
    ])

    print(f"Training TF-IDF + Logistic Regression on {args.input}...")
    model.fit(X_train, y_train)

    print("Evaluating on validation split...")
    predictions = model.predict(X_val)
    metrics = evaluate(y_val, predictions)

    model_path = MODELS / f"tfidf_logreg_{args.input}.joblib"
    result_path = RESULTS / f"validation_{args.input}.json"

    joblib.dump(model, model_path)
    result_path.write_text(
        json.dumps(
            {
                "input": args.input,
                "train_rows": len(train),
                "validation_rows": len(val),
                "label_mapping": {"0": "allow", "1": "deny"},
                "metrics": metrics,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\nValidation results")
    print(json.dumps(metrics, indent=2))
    print(f"\nModel saved to: {model_path}")
    print(f"Metrics saved to: {result_path}")


if __name__ == "__main__":
    main()
