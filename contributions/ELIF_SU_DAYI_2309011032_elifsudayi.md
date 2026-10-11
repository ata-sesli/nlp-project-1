# Elif Su Dayı: contribution

**Role:** BiLSTM modeling. I designed, built, trained, and evaluated the Bidirectional LSTM baseline models (Model A and Model B) using GloVe embeddings, evaluated them on the in-domain test set and outside test sets, and generated predictions for standardized benchmark evaluation.

## What I did

1. **Subsampling and Data Loading:** Loaded the dataset splits with `engine="python"` to avoid silent row truncation from NUL characters (affecting 31 rows). Because the full training split contains 335k rows, I downsampled a balanced subset of 40,000 training examples (20k allow, 20k deny with seed 42) to keep training time practical on GPU, while keeping validation at 5,000 rows and evaluating on the full test split (71,613 rows) and outside OOD test sets (`ood_approve_or_deny` and `ood_saroku`).
2. **Input Formulation:** Formatted inputs for both model hypotheses:
   - **Model A (Command-only):** Uses only the proposed tool call (`input_a`).
   - **Model B (Instruction + Command):** Uses the full context (`input_b`), ensuring no redundant command concatenation (`[SEP]`) since `input_b` already incorporates the tool call at the beginning.
   - Constrained sequence length to `max_len=128` tokens; since the critical command and user intent occur at the start of the prompt, 128 tokens captured the core decision boundary while maximizing throughput.
3. **Vocabulary & Pre-trained Embeddings:** Built a custom tokenizer preserving markers, yielding an effective vocabulary of 201,714 tokens (filtering singletons). Loaded pre-trained 100-dimensional Stanford GloVe embeddings (`glove.6B.100d`), mapping known words to their vectors and initializing unknown tokens with a normal distribution.
4. **Architecture Design:** Built a PyTorch `BiLSTMClassifier` with:
   - A trainable 100-dimensional GloVe embedding layer.
   - A 2-layer Bidirectional LSTM (`hidden_dim=128`, `dropout=0.3`).
   - Global Max-Pooling across sequence steps to capture the most salient classification signals.
   - Dropout (0.3) followed by a linear classification head (`hidden_dim * 2 -> 1`).
5. **Training with Early Stopping:** Trained both models using `BCEWithLogitsLoss`, Adam optimizer (`lr=1e-3`), and gradient clipping (`max_norm=5.0`). Implemented validation-loss early stopping (`patience=2`), saving best checkpoints as `bilstm_A.pt` and `bilstm_B.pt`. Both models converged within 3–4 epochs.
6. **Standardized Evaluation & Metrics:**
   - Evaluated both models on the test set:
     - **Model A (Command only):** Accuracy: 90.61%, Precision: 88.99%, Recall: 92.51%, F1-Score: 90.72%, AUROC: 0.9645, False Allow: 7.49%.
     - **Model B (Instruction + Command):** Accuracy: 95.64%, Precision: 96.17%, Recall: 95.00%, F1-Score: 95.58%, AUROC: 0.9912, False Allow: 5.00%.
   - Proved the team hypothesis: adding instruction context reduced false allowances by ~33% and raised AUROC to 0.9912.
7. **Prediction Export & Team Benchmark:**
   - Exported prediction probability CSVs (`id,label,p_deny`) for Model A, Model B, and both OOD sets (`ood_approve_or_deny` and `ood_saroku`).
   - Ran `evaluate_predictions.py` to produce standardized metric breakdowns and exported the full `results/` archive for cross-model comparison with DistilBERT and the baseline.
8. **Error Analysis:** Isolated False Positives and False Negatives from Model B predictions. Identified recurring failure modes where the model denied authorized cache clears or allowed commands leaking sensitive credentials despite user warnings.
9. **External Tests:** Contributed my assigned set of realistic, handwritten test cases (prompt + tool call pairs) to test out-of-distribution edge cases.

I used an AI assistant to help draft, debug, and optimize the PyTorch data loaders and training loop. I made the data decisions, architecture choices, and experimental evaluations above.

## Where my work is

- In this repo: `notebooks/BILSTM.ipynb` (the training and evaluation notebook), `models/` (`bilstm_A.pt`, `bilstm_B.pt`), and `results/` (evaluation outputs and prediction CSVs).
- Metric summaries, confusion matrix heatmaps, and failure analysis examples provided for the team presentation.