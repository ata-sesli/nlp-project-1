"""Shared evaluation utilities for binary classification."""

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def evaluate(y_true, y_pred):
    """Calculate accuracy, positive-class metrics, and confusion matrix."""
    true_labels = set(y_true)
    labels = ["approve", "deny"] if "approve" in true_labels else (
        [0, 1] if 0 in true_labels else ["allow", "deny"]
    )
    positive_label = labels[0] if labels[0] == "approve" else labels[1]

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(
            y_true, y_pred, pos_label=positive_label, zero_division=0
        )),
        "recall": float(recall_score(
            y_true, y_pred, pos_label=positive_label, zero_division=0
        )),
        "f1": float(f1_score(
            y_true, y_pred, pos_label=positive_label, zero_division=0
        )),
        "confusion_matrix": confusion_matrix(
            y_true, y_pred, labels=labels
        ).tolist(),
    }
