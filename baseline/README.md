# MayI Baseline and Analysis

A reproducible baseline and evaluation pipeline for the MayI tool-call safety classification project.

This folder evaluates TF-IDF features with Logistic Regression for binary `allow`/`deny` classification.

## Models

- **input_a:** Classifies the proposed tool call.
- **input_b:** Classifies the proposed tool call with additional context.

## Methodology

- **Feature extraction:** TF-IDF with unigram and bigram features.
- **Classifier:** Logistic Regression.
- **Labels:** `0 = allow`, `1 = deny`.
- **Random seed:** `42`.
- **Evaluation splits:** Validation, test, and out-of-distribution (OOD) datasets.

## Metrics

- **Accuracy:** Fraction of all predictions that are correct.
- **Deny precision:** Fraction of predicted `deny` cases that are actually `deny`.
- **Deny recall:** Fraction of actual `deny` cases correctly identified.
- **Deny F1:** Harmonic mean of deny precision and deny recall.
- **Macro-F1:** Unweighted average of the F1 scores for both classes.
- **False allow rate:** Fraction of actual `deny` cases incorrectly predicted as `allow`.
- **False deny rate:** Fraction of actual `allow` cases incorrectly predicted as `deny`.
- **Confusion matrix:** Counts of true negatives, false positives, false negatives, and true positives.

False allow and false deny rates use the actual class as the denominator.

## Repository Structure

- `src/`: Training and evaluation scripts.
- `results/`: Validation, test, and OOD metrics and prediction outputs.
- `models/`: Locally generated model artifacts; model files are excluded from Git.

## Requirements

Python 3.10 or newer is recommended. Install the dependencies listed in `requirements.txt`.

## Setup

Clone the team repository and enter this folder:

```bash
git clone https://github.com/ata-sesli/nlp-project-1.git
cd nlp-project-1/baseline
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Dataset Setup

The dataset is in the same repository, under `dataset/`. The training and evaluation scripts read the compressed CSV files from `dataset/data/`, so no separate download is needed. See `dataset/README.md` for data preparation details and licensing information.

## Running the Pipeline

Run the commands from this folder (`baseline/`), with the virtual environment activated.

### 1. Train the baselines

```bash
python src/baseline.py --input input_a
python src/baseline.py --input input_b
```

These commands train the models and produce validation metrics. The generated model files are stored locally under `models/`.

### 2. Evaluate on the test split

```bash
python src/evaluate_baseline.py
```

This evaluates both models on the test split and writes metrics to `results/test_baselines.json`. It also saves per-example predictions and deny probabilities to `results/pred_test_input_a.csv` and `results/pred_test_input_b.csv`.

### 3. Evaluate on OOD datasets

```bash
python src/evaluate_ood.py
```

This evaluates the models on the available out-of-distribution datasets and writes results to `results/ood_baselines.json`.

### 4. Generate the summary

```bash
python src/summarize_baseline.py
```

This combines validation, test, and OOD metrics into `results/baseline_summary.csv`.

## Results

See `results/baseline_summary.csv` for the consolidated metrics. The JSON files in `results/` contain the underlying evaluation results.

OOD results should be interpreted separately from test results because distribution shifts can substantially affect model performance.

## Scope and Limitations

This folder contains the baseline and analysis component, not the complete MayI project.

The models use conventional text features and Logistic Regression. Strong performance on the standard test split does not guarantee robust performance on unseen distributions or establish that a model is safe for deployment.

The trained model artifacts are excluded from Git. Reproduce them locally using the training commands above.
