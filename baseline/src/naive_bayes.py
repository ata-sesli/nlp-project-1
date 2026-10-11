"""Word and character TF-IDF + Multinomial Naive Bayes experiments."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from evaluate import evaluate

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT.parent / "dataset" / "data"
MODELS = ROOT / "models"
RESULTS = ROOT / "results"
OUTPUT = RESULTS / "nb_baselines.json"


def load_split(name):
    files = sorted(DATA.glob(f"{name}*.csv.gz"))
    if not files:
        raise FileNotFoundError(f"No files found for split: {name}")
    return pd.concat([pd.read_csv(path) for path in files], ignore_index=True)


def main():
    MODELS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    train = load_split("train")
    val = load_split("val")
    y_train = train["label"].astype(int)
    y_val = val["label"].astype(int)
    all_results = {}

    for input_name in ("input_a", "input_b"):
        X_train = train[input_name].fillna("").astype(str)
        X_val = val[input_name].fillna("").astype(str)

        for feature_type in ("word", "char"):
            name = f"nb_{feature_type}_{input_name}"
            model_path = MODELS / f"{name}.joblib"

            if model_path.exists():
                print(f"Loading existing {name}...", flush=True)
                model = joblib.load(model_path)
            else:
                print(f"Training {name}...", flush=True)

                if feature_type == "word":
                    vectorizer = TfidfVectorizer(
                        lowercase=True,
                        ngram_range=(1, 2),
                        min_df=2,
                        max_features=100_000,
                        sublinear_tf=True,
                    )
                else:
                    vectorizer = TfidfVectorizer(
                        analyzer="char",
                        ngram_range=(3, 5),
                        min_df=2,
                        max_features=30_000,
                        sublinear_tf=True,
                    )

                model = Pipeline([
                    ("tfidf", vectorizer),
                    ("classifier", MultinomialNB()),
                ])
                model.fit(X_train, y_train)
                joblib.dump(model, model_path)

            predictions = model.predict(X_val)
            metrics = evaluate(y_val.tolist(), predictions.tolist())

            all_results[name] = {
                "input": input_name,
                "features": feature_type,
                "train_rows": len(train),
                "validation_rows": len(val),
                "label_mapping": {"0": "allow", "1": "deny"},
                "metrics": metrics,
            }

            OUTPUT.write_text(
                json.dumps(all_results, indent=2),
                encoding="utf-8",
            )
            print(json.dumps({name: metrics}, indent=2), flush=True)
            print(f"Saved progress to {OUTPUT}", flush=True)


if __name__ == "__main__":
    main()
