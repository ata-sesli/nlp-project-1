# MayI Baseline and Analysis

This repository contains the TF-IDF and Logistic Regression baseline
for the MayI tool-call safety classification project.

## Models

- input_a: classifies the proposed tool call.
- input_b: classifies the proposed tool call with additional context.

## Method

- TF-IDF with unigram and bigram features.
- Logistic Regression.
- Labels: 0 = allow, 1 = deny.
- Metrics: accuracy, deny precision, deny recall, deny F1,
  and confusion matrix.

## Structure

- src/: baseline and evaluation scripts.
- models/: trained model artifacts.
- results/: validation, test, and OOD evaluation results.

## Installation

Python 3.10 or newer is recommended.

Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Results

See results/baseline_summary.csv and the JSON files in results/.

## Scope

This repository contains the baseline and analysis component,
not the complete MayI project.

## Dataset setup

The dataset is maintained separately:
https://github.com/Enes-Ozbek/LucidAI-Dataset

After cloning this repository, download the dataset into the expected directory:

    git clone https://github.com/Enes-Ozbek/LucidAI-Dataset.git LucidAI-Dataset

The evaluation scripts expect the test and OOD CSV files under
`LucidAI-Dataset/data/`. See the dataset repository for its data preparation
details and licensing information.
