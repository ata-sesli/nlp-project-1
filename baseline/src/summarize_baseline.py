
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

METRIC_KEYS = [
    "accuracy",
    "deny_precision",
    "deny_recall",
    "deny_f1",
    "macro_f1",
    "false_allow_rate",
    "false_deny_rate",
]


def load_json(filename):
    path = RESULTS / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def percent(value):
    return f"{value * 100:.2f}%"


def add_row(rows, split, dataset, input_name, metrics):
    tn, fp = metrics["confusion_matrix"][0]
    fn, tp = metrics["confusion_matrix"][1]

    # Calculate macro-F1 from the confusion matrix.
    f1_allow = tn / (tn + (fp + fn) / 2) if (tn + (fp + fn) / 2) else 0
    f1_deny = tp / (tp + (fp + fn) / 2) if (tp + (fp + fn) / 2) else 0
    macro_f1 = (f1_allow + f1_deny) / 2

    row = {
        "split": split,
        "dataset": dataset,
        "input": input_name,
        "accuracy": metrics["accuracy"],
        "deny_precision": metrics["deny_precision"],
        "deny_recall": metrics["deny_recall"],
        "deny_f1": metrics["deny_f1"],
        "macro_f1": macro_f1,
        "false_allow_rate": fn / (fn + tp) if (fn + tp) else 0,
        "false_deny_rate": fp / (tn + fp) if (tn + fp) else 0,
    }

    rows.append(row)


def main():
    rows = []

    for filename in [
        "validation_input_a.json",
        "validation_input_b.json",
    ]:
        data = load_json(filename)
        add_row(
            rows,
            "Validation",
            "validation",
            data["input"],
            data["metrics"],
        )

    test_data = load_json("test_baselines.json")

    for input_name, metrics in test_data["results"].items():
        add_row(rows, "Test", "test", input_name, metrics)

    ood_data = load_json("ood_baselines.json")

    for input_name, datasets in ood_data["results"].items():
        for filename, metrics in datasets.items():
            add_row(
                rows,
                "OOD",
                filename.removesuffix(".csv.gz"),
                input_name,
                metrics,
            )

    output_path = RESULTS / "baseline_summary.csv"
    columns = ["split", "dataset", "input", *METRIC_KEYS]

    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for row in rows:
            csv_row = row.copy()
            for key in METRIC_KEYS:
                csv_row[key] = percent(csv_row[key])
            writer.writerow(csv_row)

    print("\nBASELINE RESULTS")
    print("-" * 145)
    print(
        f'{"Split":12} {"Dataset":24} {"Input":10} '
        f'{"Accuracy":10} {"Deny Prec.":11} {"Deny Recall":12} '
        f'{"Deny F1":10} {"Macro-F1":10} '
        f'{"False Allow":12} {"False Deny":12}'
    )
    print("-" * 145)

    for row in rows:
        print(
            f'{row["split"]:12} '
            f'{row["dataset"]:24} '
            f'{row["input"]:10} '
            f'{percent(row["accuracy"]):10} '
            f'{percent(row["deny_precision"]):11} '
            f'{percent(row["deny_recall"]):12} '
            f'{percent(row["deny_f1"]):10} '
            f'{percent(row["macro_f1"]):10} '
            f'{percent(row["false_allow_rate"]):12} '
            f'{percent(row["false_deny_rate"]):12}'
        )

    print("-" * 145)
    print(f"Total evaluations: {len(rows)}")
    print(f"CSV saved to: {output_path}")


if __name__ == "__main__":
    main()
