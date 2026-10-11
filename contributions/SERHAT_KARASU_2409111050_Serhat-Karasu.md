# Serhat Karasu: Contribution

**Role:** TF-IDF baseline and evaluation. I worked on the classical machine-learning baseline for the MayI project, focusing on evaluating both input formats, reporting classification metrics, and documenting the results.

## What I did

1. **Worked on the TF-IDF baseline.** Used TF-IDF features with Logistic Regression as a classical machine-learning reference for the approve-or-deny classification task.

2. **Compared both input formats.**
   - **A:** The tool call alone (`input_a`).
   - **B:** The tool call with the user's request and the agent's history (`input_b`).

3. **Implemented evaluation metrics.** Worked on evaluation scripts for accuracy, deny-class precision, recall and F1-score, confusion matrices, macro-F1, false-allow rate, and false-deny rate.

4. **Prepared per-example test predictions.** Added prediction outputs containing `id`, `label`, `prediction`, and `p_deny` to support error analysis and comparison with other model evaluations.

5. **Reviewed baseline results.** The reported test-split macro-F1 scores were 0.9069 for A and 0.9410 for B, indicating better performance for the contextual input format on this split.

6. **Documented the baseline.** Prepared documentation covering the approach, input formats, evaluation metrics, datasets, limitations, and expected output artifacts.

## Future work

- Add AUROC evaluation using `p_deny`.
- Generate prediction files for both external test datasets.
- Align dataset paths and execution instructions with the shared repository.
- Validate the complete pipeline and document reproducible results.

The TF-IDF baseline provides a classical machine-learning reference point for comparison with the project's transformer-based models.
