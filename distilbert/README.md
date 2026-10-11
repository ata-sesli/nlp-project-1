# DistilBERT

Fine-tunes `distilbert-base-uncased` to label an agent's proposed tool call **allow (0)** or
**deny (1)**, in two input formats from the cleaned dataset:

- **A** (`input_a`): the tool call alone.
- **B** (`input_b`): the tool call, the user's request and the agent's earlier steps.

Comparing A and B measures how much the context helps. Both formats are used exactly as the
[cleaned dataset](../dataset) provides them, and both models
are trained on the full training split (335,349 rows).

Published models: [`akifkulll/mayi-distilbert-a`](https://huggingface.co/akifkulll/mayi-distilbert-a)
and [`akifkulll/mayi-distilbert-b`](https://huggingface.co/akifkulll/mayi-distilbert-b).

The task is inspired by [MayI](https://github.com/ata-sesli/MayI), which approves or holds coding
agents' tool calls. This project is a standalone classifier and benchmark; it is not wired into
MayI.

## Files

| file | what it does |
|---|---|
| `distilbert_colab.ipynb` | Trains A and B (Colab, A100), scores them and publishes them to the Hub. Kept with its outputs. |
| `train_distilbert.py` | Trains one model and writes `model/`, `predictions/<split>.csv` (`id, label, p_deny`) and `run.json` (settings, time, speed). |
| `evaluate_predictions.py` | Scores any `id, label, p_deny` file: metrics overall and by length, difficulty and framework, a confusion matrix and the 200 most confident mistakes. Works for every model in the project. |
| `push_to_hub.py` | Uploads a trained model and its model card to the Hugging Face Hub. |
| `predict.py` | Loads a model from the Hub (or a folder) and scores one text or a whole CSV. |
| `Dockerfile`, `requirements.txt` | A CPU image that runs `predict.py`; the model is downloaded at run time. |
| `results/` | `metrics.md`, `metrics.json` and a confusion matrix for each model and split, plus each run's `run.json`. |

## Training setup

| | A | B |
|---|---|---|
| train rows | 335,349 (all) | 335,349 (all) |
| max tokens | 128 | 512 |
| batch size | 64 | 32 |
| learning rate | 3e-5, 6% linear warm-up, linear decay | same |
| epochs | 1 | 1 |
| model selection | best macro-F1 on a 5,000-row val sample | same |
| hardware | Colab A100 | Colab A100, 11.6 min of training |

## Results (test split, 71,613 rows, threshold 0.5)

Adding the user's request and the agent's history cuts the false allow rate from 8.8% to 4.1%.

| model | accuracy | macro-F1 | false allow rate | false deny rate | AUROC |
|---|---:|---:|---:|---:|---:|
| A (call only) | 0.9142 | 0.9142 | 0.0879 | 0.0837 | 0.9685 |
| **B (call + context)** | **0.9607** | **0.9607** | **0.0405** | **0.0381** | **0.9929** |

### Calls that appear with both labels

4,201 test rows have a tool call that is allowed with one request and denied with another, so
only the context can decide them. Here the call-only model is close to a coin flip:

| model | macro-F1 |
|---|---:|
| A (call only) | 0.5971 |
| **B (call + context)** | **0.8971** |

### Outside test sets (written separately from the training data)

| model | approve-or-deny macro-F1 | saroku macro-F1 |
|---|---:|---:|
| A (call only) | 0.8763 | 0.6574 |
| **B (call + context)** | **0.9216** | **0.7390** |

saroku is written in a different format (CONTEXT and RULES sections) and remains the weakest set:
a domain-shift limit of training on one synthetic source.

**Metric choice.** The data is balanced (about 50% deny), so accuracy is not misleading, but we
rank by **macro-F1**, which weighs both classes equally. The two errors do not cost the same:
letting a harmful call through is worse than blocking a safe one, so we also report the **false
allow rate** (share of deny rows predicted allow). **AUROC** shows how well the scores separate
the classes before any threshold is chosen.

Full breakdowns are in `results/`.

## Limitations

- Model B was trained with the agent's history. A tool that cannot supply the history (MayI
  currently sends none) needs a history-free variant.
- Labels were written by AI models, not people, and the data is synthetic: the weaker saroku
  results show the cost of a different input format.
- One training run per model (seed 42); variance across seeds was not measured.

## Reproduce

Training: open `distilbert_colab.ipynb` in Colab with an A100 GPU and run all cells (B about 12
minutes of training, A a few minutes).

Scoring with the published model, no GPU needed:

```bash
docker build -t mayi-distilbert .
echo "### PROPOSED TOOL CALL ..." | docker run -i --rm -v hf-cache:/cache mayi-distilbert --text -
docker run --rm -v hf-cache:/cache -v "$PWD/data:/data" mayi-distilbert \
    --input /data/test.csv.gz --out /data/predictions/test.csv
```

Use the A model with `-e MODEL_ID=akifkulll/mayi-distilbert-a ... --text-col input_a`.
Checked on a laptop CPU with Docker Desktop: the outside test set `ood_approve_or_deny`
(1,448 rows) gives accuracy 0.9220 with the published B model, the same as on the Colab GPU. CPU
speed for B is about 8 rows/s (A100: over 1,000 rows/s), so score a sample before a whole split.
