# Ata Sesli: contribution

**Role:** the benchmark and the team repository. I proposed the task, built the benchmark that
scores every model the same way, and brought the team's separate work into one repo. My code is
in the `benchmark/` folder.

## What I did

1. **Proposed the task.** The idea comes from my own project,
   [MayI](https://github.com/ata-sesli/MayI), which approves or holds the tool calls of coding
   agents. For this course we turned its core question into a text classification task: given
   the action an agent wants to take, should it be allowed or denied? This project is a
   standalone classifier and benchmark; it is not wired into MayI.
2. **Designed the benchmark around one predictions format** (`benchmark/common.py`). Every model
   writes `id, label, p_deny` for each split, and the benchmark reads only those files. A new
   model needs one small scorer and nothing else changes. The same file holds the model list,
   which keeps the architecture (for example DistilBERT) apart from the specific model
   (`distilbert-base-uncased`, fine-tuned).
3. **Wrote a scorer for each model family:**
   - `benchmark/score_baseline.py` for the TF-IDF + Logistic Regression models (A and B).
   - `benchmark/score_distilbert.py` for the fine-tuned DistilBERT models (A and B), loaded from
     the Hugging Face Hub. It reuses the scoring code of `distilbert/predict.py`.

   Both take `--limit N`, which scores a fixed random sample (seed 42) that is the same rows for
   every model, so a quick run on a laptop CPU stays a fair comparison.
4. **Wrote the benchmark script** (`benchmark/run_benchmark.py`). It scores every model on the
   test split and the two outside test sets with one metric function, the one in
   `distilbert/evaluate_predictions.py`, so no model is measured differently. It writes:
   - `benchmark.csv`: macro-F1, accuracy, false allow rate, false deny rate, AUROC and the
     confusion counts for each model and split.
   - `benchmark_by_group.csv`: the test split by difficulty and by whether the same command
     appears with both labels.
   - Charts: A against B for macro-F1 and for the false allow rate, macro-F1 against CPU time,
     macro-F1 by difficulty, and the confusion matrices.
5. **Added a CPU latency measurement** (`measure_latency` in `benchmark/common.py`): the time for
   one row, one row per call, on 200 fixed test rows, reported as the median and the 95th
   percentile. It shows the trade between accuracy and speed.
6. **Brought the team's work into one repo.** The DistilBERT and baseline parts were written in
   separate repositories. I moved each into its own folder (`distilbert/`, `baseline/`) and kept
   every teammate's commits under their own name, so the history shows who wrote what.
7. **Made the parts work together.** The baseline scripts and the DistilBERT scripts and
   notebook read the data from a separate dataset repo; I pointed them at `dataset/data/` in
   this repo, so one clone is enough to run everything.
8. **Documentation:** `benchmark/README.md`, which explains how the benchmark works, how to run
   it and why we chose these metrics.

I used Claude, an AI assistant, to help write and check the code. I made the decisions above.
