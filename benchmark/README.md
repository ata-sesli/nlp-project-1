# Benchmark

Scores every model in the project the same way: on the test split and the two outside test
sets, with one metric function, plus the CPU time each model needs per row.

## How it works

1. A scorer per model family writes its predictions in one shared format:
   `predictions/<model>/<split>.csv` with the columns `id, label, p_deny`, and
   `predictions/<model>/latency.json`.
2. `run_benchmark.py` reads those files and builds the tables and charts in `results/`.

`predictions/` is not in the repo (it is rebuilt by the scorers); `results/` is.

Every scorer takes `--limit N`, which scores a fixed random sample of N rows per split (seed 42).
The sample is the same rows for every model, so the models stay comparable.

## Files

| file | what it does |
|---|---|
| `common.py` | The model list, data loading, the predictions format and the latency measurement. |
| `score_baseline.py` | Scores the TF-IDF + Logistic Regression models (A and B). |
| `score_distilbert.py` | Scores the fine-tuned DistilBERT models (A and B) from the Hugging Face Hub. |
| `score_julia.py` | Scores [Julia 1](https://huggingface.co/SupersonicLabs/Julia-1), a general decision model, zero-shot (A and B). It is our "new method": it is asked a yes/no question and is not trained on our data. |
| `run_benchmark.py` | Builds `results/benchmark.csv`, `benchmark_by_group.csv`, `benchmark.md` and the charts. |
| `requirements.txt` | Packages the scripts need. |

## Run

From the repo's root folder:

```bash
pip install -r benchmark/requirements.txt

python baseline/src/baseline.py --input input_a   # trains the baseline models,
python baseline/src/baseline.py --input input_b   # which are not in the repo
python benchmark/score_baseline.py --limit 1000

python benchmark/score_distilbert.py --limit 1000  # drop --limit from both for every row (GPU recommended)

python -c "from huggingface_hub import snapshot_download; snapshot_download('SupersonicLabs/Julia-1', local_dir='Julia-1')"
pip install -e ./Julia-1                           # about 550 MB; needs Python 3.11+
python benchmark/score_julia.py --model-dir Julia-1 --limit 1000

python benchmark/run_benchmark.py
```

## Metrics

Deny is the positive class and a row is denied when `p_deny >= 0.5`.

- **Macro-F1** ranks the models. The data is balanced (about half of every split is deny), and
  macro-F1 weighs both classes equally.
- **False allow rate** is the share of deny rows predicted allow. Letting a harmful call through
  costs more than blocking a safe one, so this error is reported on its own.
- **AUROC** shows how well the scores separate the classes before any threshold is chosen.
- **Latency** is the time for one row on the CPU, one row per call, on 200 fixed test rows
  (median and 95th percentile).
