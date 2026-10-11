"""Shared evaluation utilities for NLP experiments."""

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def evaluate(y_true, y_pred):
    """Calculate classification metrics for approve/deny predictions."""
    labels = ["approve", "deny"]

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(
            y_true, y_pred, pos_label="approve", zero_division=0
        ),
        "recall": recall_score(
            y_true, y_pred, pos_label="approve", zero_division=0
        ),
        "f1": f1_score(
            y_true, y_pred, pos_label="approve", zero_division=0
        ),
        "confusion_matrix": confusion_matrix(
            y_true, y_pred, labels=labels
        ).tolist(),
    }
