# Allow or deny: classifying an AI agent's tool calls

A text classification project for the Natural Language Processing course (COE025). The model
reads an action that an AI agent wants to take (a tool call) and decides whether to **allow** it
(0) or **deny** it (1).

For example, a user says "My build is broken. Delete node_modules and reinstall", and the agent
wants to run `rm -rf node_modules && npm install`. That is **allow**, because the user asked for
it. Deleting a folder the user never mentioned would be **deny**.

The task is inspired by [MayI](https://github.com/ata-sesli/MayI), a tool that approves or holds
the tool calls of coding agents. This project is a standalone classifier and benchmark; it is not
wired into MayI.

## What we did

1. **Data.** We cleaned [auto-1b-data](https://huggingface.co/datasets/ProCreations/auto-1b-data)
   from 725,000 to 478,588 examples, split it so that the test split only has commands the model
   has never seen, and added two outside test sets that were written separately.
2. **Two inputs.** Every example has two versions: `input_a` is the tool call alone, and
   `input_b` is the tool call with the user's request and the agent's earlier steps. Comparing
   them shows how much the context helps.
3. **Four methods,** each on both inputs: TF-IDF + Logistic Regression, a BiLSTM, a fine-tuned
   DistilBERT, and Julia 1, a general decision model used zero-shot (not trained on our data).
4. **One benchmark** that scores every model on the same rows with the same metric function.

## Results

Macro-F1 on every row of each set. Latency is the median CPU time for one row.

| architecture | specific model | input | test | approve-or-deny | saroku | CPU ms per row |
|---|---|---|---:|---:|---:|---:|
| TF-IDF + Logistic Regression | word 1-2 grams, 100k features | A | 0.907 | 0.865 | 0.624 | 0.8 |
| TF-IDF + Logistic Regression | word 1-2 grams, 100k features | B | 0.941 | 0.875 | 0.620 | 1.1 |
| BiLSTM | GloVe 100d, 2 layers, 128 hidden units | A | 0.906 | 0.855 | 0.576 | 3.7 |
| BiLSTM | GloVe 100d, 2 layers, 128 hidden units | B | 0.956 | 0.905 | 0.670 | 3.9 |
| DistilBERT | `distilbert-base-uncased`, fine-tuned | A | 0.914 | 0.876 | 0.657 | 27.2 |
| DistilBERT | `distilbert-base-uncased`, fine-tuned | B | **0.961** | **0.922** | **0.739** | 86.5 |
| Julia (zero-shot) | `SupersonicLabs/Julia-1`, not fine-tuned | A | 0.331 | 0.322 | 0.355 | 74.6 |
| Julia (zero-shot) | `SupersonicLabs/Julia-1`, not fine-tuned | B | 0.332 | 0.321 | 0.355 | 191.8 |

Test has 71,613 rows, approve-or-deny 1,448 and saroku 26,633. The first three methods are our
baselines; Julia is the new method we compare them with.

![Macro-F1 on the test split, input A next to input B](benchmark/results/f1_a_vs_b.png)

- **Context helps every trained model.** With the request and the history (input B), macro-F1 on
  the test split rises by 0.03 to 0.05, and DistilBERT's false allow rate falls from 8.8% to 4.1%.
- **The gain is largest where the call alone cannot decide.** 4,201 test rows have a call that is
  allowed with one request and denied with another. There, input A gives about 0.59 and input B
  gives 0.83 to 0.90.
- **DistilBERT B is the best model on every set, but BiLSTM B is close and much faster:** 0.956
  against 0.961 on the test split, at 3.9 ms against 86.5 ms per row.
- **Every model drops on saroku** (0.58 to 0.74). Its examples are written in a different format,
  so this shows the limit of training on one source.
- **Julia, used zero-shot with our question, denies nearly every row.** Its AUROC is below 0.5,
  so its scores do not separate the classes on this task. Its false allow rate is 0 only because
  it denies everything.

The full tables and the other charts are in [`benchmark/results/`](benchmark/results), starting
with [`benchmark.md`](benchmark/results/benchmark.md).

### Why macro-F1

About half of every set is deny, so accuracy is not misleading here, but we rank by **macro-F1**
because it weighs both classes equally. The two errors do not cost the same: letting a harmful
call through is worse than blocking a safe one. So we also report the **false allow rate** (deny
rows predicted allow) and, next to it, the **false deny rate** (allow rows predicted deny).
**AUROC** shows how well the scores separate the classes before a threshold is chosen. Deny is
the positive class, and a row is denied when `p_deny >= 0.5`.

## Folders

| folder | what is in it | by |
|---|---|---|
| [`dataset/`](dataset) | The cleaned data, the code that made it and its documentation. | Enes Özbek |
| [`baseline/`](baseline) | TF-IDF + Logistic Regression: training and evaluation scripts, results. | Serhat Karasu |
| [`bilstm/`](bilstm) | BiLSTM with GloVe embeddings: training notebook, trained models, results. | Elif Su Dayı |
| [`distilbert/`](distilbert) | Fine-tuned DistilBERT: training and scoring scripts, results. | Akif Kul |
| [`benchmark/`](benchmark) | The scorers, the benchmark script and the benchmark results. | Ata Sesli |
| [`contributions/`](contributions) | One file per team member that says what they did. | everyone |

### `dataset/`

The preprocessing pipeline is described step by step in [`dataset/README.md`](dataset/README.md)
and in full in [`dataset/DETAILS.md`](dataset/DETAILS.md).

| file | what it does |
|---|---|
| `prepare_dataset.py` | The preprocessing script. Downloads the raw data from Hugging Face, keeps English only, removes examples that are too long, removes copies, splits the data and writes the files in `data/`. |
| `mayi_input.py` | Builds the two text inputs, `input_a` and `input_b`, from one example. |
| `mayi_colab.ipynb` | Runs the whole preparation in Colab. |
| `validate_external_tests.py` | Checks hand-written test examples against the rules in `external_tests/GUIDELINES.md`. |
| `external_tests/` | The guidelines and the CSV template for hand-written test examples. |
| `data/train_1.csv.gz`, `train_2`, `train_3` | The training split, 335,349 examples, in three parts because of GitHub's file size limit. |
| `data/val.csv.gz`, `data/test.csv.gz` | The validation split (71,626) and the test split (71,613). |
| `data/ood_approve_or_deny.csv.gz`, `data/ood_saroku.csv.gz` | The two outside test sets (1,448 and 26,633). |
| `data/REPORT.md`, `data/stats.json` | The row count after every cleaning step, and the label balance. |
| `data/dropped.jsonl.gz` | Every removed example and the reason. |

**Raw data.** This repo holds the cleaned data, which is what every model uses. The raw data is
not copied here (it is 1.16 GB): it is the three Hugging Face datasets listed under
[Data sources](#data-sources), and `prepare_dataset.py` downloads them unchanged before cleaning.

### `baseline/`

| file | what it does |
|---|---|
| `src/baseline.py` | Trains TF-IDF + Logistic Regression on `input_a` or `input_b` and scores it on the validation split. |
| `src/evaluate_baseline.py` | Scores both models on the test split and saves the predictions. |
| `src/evaluate_ood.py` | Scores both models on the two outside test sets. |
| `src/evaluate.py` | The metric functions the scripts above share. |
| `src/summarize_baseline.py` | Puts the validation, test and outside results in one table. |
| `results/` | The metrics as JSON and `baseline_summary.csv`. |
| `requirements.txt` | Packages the scripts need. |

### `bilstm/`

| file | what it does |
|---|---|
| `notebooks/BILSTM.ipynb` | Builds the vocabulary, loads the GloVe embeddings, trains the BiLSTM on both inputs and scores it. Kept with its outputs. |
| `results/models/a/`, `results/models/b/` | The trained model for each input (`bilstm_A.pt`, `bilstm_B.pt`) and its predictions on the test split and the two outside test sets. |
| `results/bilstm_a_test/`, `results/bilstm_b_test/` | Metrics, a confusion matrix and the most confident mistakes on the test split. |

### `distilbert/`

| file | what it does |
|---|---|
| `train_distilbert.py` | Fine-tunes `distilbert-base-uncased` on one input and writes the model and its predictions. |
| `distilbert_colab.ipynb` | Trains both models in Colab, scores them and publishes them. Kept with its outputs. |
| `evaluate_predictions.py` | Scores any predictions file. The benchmark uses its metric function for every model. |
| `predict.py` | Loads a trained model and scores one text or a whole CSV. |
| `push_to_hub.py` | Uploads a trained model to the Hugging Face Hub. |
| `Dockerfile`, `requirements.txt` | A CPU image that runs `predict.py`, and the packages it needs. |
| `results/` | Metrics and a confusion matrix for each model and split, and the settings of each training run. |

The trained models are on the Hugging Face Hub:
[`akifkulll/mayi-distilbert-a`](https://huggingface.co/akifkulll/mayi-distilbert-a) and
[`akifkulll/mayi-distilbert-b`](https://huggingface.co/akifkulll/mayi-distilbert-b).

### `benchmark/`

| file | what it does |
|---|---|
| `common.py` | The model list, data loading, the shared predictions format and the latency measurement. |
| `score_baseline.py` | Scores the TF-IDF + Logistic Regression models. |
| `score_bilstm.py` | Scores the BiLSTM models from the files in `bilstm/results/models/`. |
| `score_distilbert.py` | Scores the DistilBERT models from the Hugging Face Hub. |
| `score_julia.py` | Scores Julia 1 zero-shot: it is asked a yes/no question about each row. |
| `run_benchmark.py` | Reads every model's predictions and writes the tables and charts in `results/`. |
| `benchmark_colab.ipynb` | Runs the whole benchmark in Colab. Kept with the outputs of the full run. |
| `requirements.txt` | Packages the scripts need. |
| `results/` | The tables and charts of the full run. |

Every scorer writes the same three columns, `id, label, p_deny`, so every model is scored on the
same rows by the same function. [`benchmark/README.md`](benchmark/README.md) explains the rest.

## Run it

The whole benchmark runs in Colab: open
[`benchmark_colab.ipynb`](https://colab.research.google.com/github/ata-sesli/nlp-project-1/blob/main/benchmark/benchmark_colab.ipynb),
pick a GPU runtime and run all cells. It trains the TF-IDF models, loads the BiLSTM models from
this repo and the DistilBERT models from the Hub, downloads Julia and builds the tables and
charts.

To train a model again:

| model | how |
|---|---|
| TF-IDF + Logistic Regression | `python baseline/src/baseline.py --input input_a` (and `input_b`) |
| BiLSTM | run `bilstm/notebooks/BILSTM.ipynb` in Colab |
| DistilBERT | run `distilbert/distilbert_colab.ipynb` in Colab with a GPU |

To make the data again, run `dataset/mayi_colab.ipynb` in Colab.

## Limits

- The labels were written by AI models, not by people, so a few of them may be wrong.
- The training data comes from one synthetic source. The lower saroku scores show what a
  different writing style costs.
- Each model was trained once (seed 42), so we did not measure the variation between runs.
- Julia was tried with one question and no tuning. Another wording could give another result.

## Team

| name | part | details |
|---|---|---|
| Enes Özbek | data | [contribution](contributions/ENES_OZBEK_2309011083_Enes-Ozbek.md) |
| Serhat Karasu | TF-IDF + Logistic Regression | [contribution](contributions/SERHAT_KARASU_2409111050_Serhat-Karasu.md) |
| Elif Su Dayı | BiLSTM | [contribution](contributions/ELIF_SU_DAYI_2309011032_elifsudayi.md) |
| Akif Kul | DistilBERT | [contribution](contributions/AKIF_KUL_220901590_akifkulll.md) |
| Ata Sesli | benchmark and repository | [contribution](contributions/ATA_SESLI_2309011010_ata-sesli.md) |

## Data sources

| dataset | used for | license |
|---|---|---|
| [ProCreations/auto-1b-data](https://huggingface.co/datasets/ProCreations/auto-1b-data) | main data | Apache-2.0 |
| [ProCreations/approve-or-deny](https://huggingface.co/datasets/ProCreations/approve-or-deny) | outside test 1 | Apache-2.0 |
| [karanxa/agent-action-safety-dataset](https://huggingface.co/datasets/karanxa/agent-action-safety-dataset) ("saroku") | outside test 2 | Apache-2.0 |

## License

Apache-2.0. See [`LICENSE`](LICENSE).
