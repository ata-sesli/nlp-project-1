
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
]


def load_json(filename):
    path = RESULTS / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def percent(value):
    return f"{value * 100:.2f}%"


def add_row(rows, split, dataset, input_name, metrics):
    row = {
        "split": split,
        "dataset": dataset,
        "input": input_name,
    }

    for key in METRIC_KEYS:
        row[key] = metrics[key]

    rows.append(row)


def main():
    rows = []

    # Validation files store metrics under the "metrics" key.
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

    # Test file stores metrics under results -> input_a/input_b.
    test_data = load_json("test_baselines.json")

    for input_name, metrics in test_data["results"].items():
        add_row(
            rows,
            "Test",
            "test",
            input_name,
            metrics,
        )

    # OOD file stores results -> input -> dataset -> metrics.
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

    # Save a CSV summary.
    output_path = RESULTS / "baseline_summary.csv"
    columns = [
        "split",
        "dataset",
        "input",
        *METRIC_KEYS,
    ]

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

    # Print a readable summary.
    print("\nBASELINE RESULTS")
    print("-" * 92)

    print(
        f'{"Split":12} {"Dataset":24} {"Input":10} '
        f'{"Accuracy":12} {"Deny Precision":16} '
        f'{"Deny Recall":13} {"Deny F1":10}'
    )

    print("-" * 92)

    for row in rows:
        print(
            f'{row["split"]:12} '
            f'{row["dataset"]:24} '
            f'{row["input"]:10} '
            f'{percent(row["accuracy"]):12} '
            f'{percent(row["deny_precision"]):16} '
            f'{percent(row["deny_recall"]):13} '
            f'{percent(row["deny_f1"]):10}'
        )

    print("-" * 92)
    print(f"Total evaluations: {len(rows)}")
    print(f"CSV saved to: {output_path}")


if __name__ == "__main__":
    main()
