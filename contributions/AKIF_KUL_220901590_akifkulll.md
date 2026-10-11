# Akif Kul: contribution

**Role:** the DistilBERT model. I fine-tuned it on both input formats, built the evaluation
script the team can share, published the models and packaged them in Docker. Everything I made
is in the `distilbert/` folder.

## What I did

1. **Fine-tuned DistilBERT** (`distilbert/train_distilbert.py`): `distilbert-base-uncased` with a
   two-class head, trained on the full training split (335,349 rows) for each input format:
   - **A**, the tool call alone (128 tokens).
   - **B**, the tool call with the user's request and the agent's history (512 tokens).

   Settings: learning rate 3e-5 with a 6% linear warm-up and linear decay, one epoch, fp16, best
   checkpoint chosen by macro-F1 on a 5,000-row validation sample. The script saves checkpoints so
   a disconnected Colab session resumes where it stopped, and writes every prediction as
   `id, label, p_deny`.
2. **Ran the training** on Colab (`distilbert/distilbert_colab.ipynb`, kept with its outputs).
   B trained in 11.6 minutes on an A100.
3. **Wrote the shared evaluation script** (`distilbert/evaluate_predictions.py`). It scores any
   `id, label, p_deny` file the same way: accuracy, macro-F1, false allow rate, false deny rate
   and AUROC, broken down by length, difficulty, framework and by whether the same command
   appears with both labels, plus a confusion matrix and the most confident mistakes. I checked
   its numbers against scikit-learn.
4. **Chose and justified the metrics.** The data is balanced, so we rank by macro-F1, and report
   the false allow rate separately because letting a harmful call through costs more than
   blocking a safe one.
5. **Benchmarked both models** on the test split and the two outside test sets
   (`distilbert/results/`). Main findings:
   - B beats A on every set; the false allow rate on the test split falls from 8.8% to 4.1%.
   - On the 4,201 test rows whose command appears with both labels, A is close to a coin flip
     (macro-F1 0.60) while B reaches 0.90: only the context can decide these rows.
   - The 512-token cut barely affects B: macro-F1 is 0.963, 0.960 and 0.959 for short, medium
     and long histories.
   - saroku, written in a different format, stays the weakest set (macro-F1 0.74 for B).
6. **Published the models** on the Hugging Face Hub with model cards
   (`distilbert/push_to_hub.py`):
   [`akifkulll/mayi-distilbert-a`](https://huggingface.co/akifkulll/mayi-distilbert-a) and
   [`akifkulll/mayi-distilbert-b`](https://huggingface.co/akifkulll/mayi-distilbert-b).
7. **Packaged inference in Docker** (`distilbert/predict.py`, `distilbert/Dockerfile`). The image
   downloads the model from the Hub at run time and scores one text or a whole CSV on a CPU. I
   ran it on my laptop: the approve-or-deny outside test set gives accuracy 0.9220, the same as
   on the Colab GPU.
8. **Team consistency checks:** confirmed that every model uses the dataset's `input_a` and
   `input_b` columns unchanged and the same splits, so the results can be compared.
9. **Documentation:** `distilbert/README.md`.

I used Claude, an AI assistant, to help write and check the code. I ran the training, the
evaluations, the Hugging Face upload and the Docker test myself.
