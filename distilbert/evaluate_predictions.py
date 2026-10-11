"""Score a predictions file (id, label, p_deny) against the dataset and break the results down.

Works for any model that writes the same columns, so the whole team can use one scorer:
    python evaluate_predictions.py --pred runs/distilbert_b/predictions/test.csv \
        --data-dir LucidAI-Dataset/data --split test --out results/distilbert_b_test

Writes metrics.json, metrics.md, confusion_matrix.png and errors.csv (most confident mistakes,
with category and rationale for error analysis) to --out.
"""

import argparse
import glob
import json
import os

import numpy as np
import pandas as pd

GROUPS = ["length_bucket", "difficulty", "call_has_both_labels", "framework"]


def metrics(y, p, threshold):
    pred = (p >= threshold).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum()); tn = int(((pred == 0) & (y == 0)).sum())
    f1_deny = 2 * tp / max(1, 2 * tp + fp + fn)
    f1_allow = 2 * tn / max(1, 2 * tn + fn + fp)
    out = {"rows": int(len(y)), "accuracy": (tp + tn) / max(1, len(y)),
           "macro_f1": (f1_deny + f1_allow) / 2, "f1_deny": f1_deny,
           "deny_recall": tp / max(1, tp + fn), "deny_precision": tp / max(1, tp + fp),
           "false_allow_rate": fn / max(1, tp + fn),   # harmful calls let through
           "false_deny_rate": fp / max(1, fp + tn),    # safe calls blocked
           "confusion": {"tn": tn, "fp": fp, "fn": fn, "tp": tp}}
    out["auroc"] = auroc(y, p)
    return out


def auroc(y, p):
    """Probability that a random deny row scores higher than a random allow row (ties count half)."""
    pos, neg = int(y.sum()), int(len(y) - y.sum())
    if pos == 0 or neg == 0:
        return None
    ranks = pd.Series(p).rank(method="average").to_numpy()
    return float((ranks[y == 1].sum() - pos * (pos + 1) / 2) / (pos * neg))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--data-dir", default="LucidAI-Dataset/data")
    ap.add_argument("--split", required=True, help="val, test, ood_approve_or_deny or ood_saroku")
    ap.add_argument("--out", required=True)
    ap.add_argument("--threshold", type=float, default=0.5, help="deny when p_deny >= threshold")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    pred = pd.read_csv(a.pred)
    files = sorted(glob.glob(os.path.join(a.data_dir, f"{a.split}*.csv.gz")))
    meta = pd.concat([pd.read_csv(f, engine="python", usecols=["id", "category", "rationale", "input_a"] + GROUPS)
                      for f in files], ignore_index=True)
    df = pred.merge(meta, on="id", how="left", validate="one_to_one")
    y, p = df["label"].to_numpy(), df["p_deny"].to_numpy()

    report = {"split": a.split, "threshold": a.threshold, "overall": metrics(y, p, a.threshold), "groups": {}}
    for g in GROUPS:
        if df[g].notna().any():
            report["groups"][g] = {str(k): metrics(sub["label"].to_numpy(), sub["p_deny"].to_numpy(), a.threshold)
                                   for k, sub in df.groupby(g)}
    with open(os.path.join(a.out, "metrics.json"), "w") as f:
        json.dump(report, f, indent=2)

    keys = ["rows", "accuracy", "macro_f1", "false_allow_rate", "false_deny_rate", "auroc"]
    fmt = lambda m: " | ".join(str(m[k]) if k == "rows" else ("-" if m[k] is None else f"{m[k]:.4f}") for k in keys)
    lines = [f"# {a.split} (threshold {a.threshold})", "", "| group | " + " | ".join(keys) + " |",
             "|---|" + "---:|" * len(keys), f"| **overall** | {fmt(report['overall'])} |"]
    for g, vals in report["groups"].items():
        for k, m in vals.items():
            lines.append(f"| {g}={k} | {fmt(m)} |")
    with open(os.path.join(a.out, "metrics.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    wrong = df[(p >= a.threshold).astype(int) != y].copy()
    wrong["confidence_in_wrong_answer"] = np.where(wrong["label"] == 1, 1 - wrong["p_deny"], wrong["p_deny"])
    wrong.sort_values("confidence_in_wrong_answer", ascending=False).head(200)[
        ["id", "label", "p_deny", "category", "difficulty", "length_bucket", "input_a", "rationale"]
    ].to_csv(os.path.join(a.out, "errors.csv"), index=False)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        c = report["overall"]["confusion"]
        m = np.array([[c["tn"], c["fp"]], [c["fn"], c["tp"]]])
        fig, ax = plt.subplots(figsize=(4, 3.6))
        ax.imshow(m, cmap="Purples")
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{m[i, j]:,}", ha="center", va="center",
                        color="white" if m[i, j] > m.max() / 2 else "black")
        ax.set_xticks([0, 1], ["allow", "deny"]); ax.set_yticks([0, 1], ["allow", "deny"])
        ax.set_xlabel("predicted"); ax.set_ylabel("true"); ax.set_title(a.split)
        fig.tight_layout(); fig.savefig(os.path.join(a.out, "confusion_matrix.png"), dpi=150)
    except ImportError:
        pass

    o = report["overall"]
    print(f"{a.split}: acc={o['accuracy']:.4f} macro_f1={o['macro_f1']:.4f} "
          f"false_allow={o['false_allow_rate']:.4f} auroc={o['auroc']:.4f} -> {a.out}")


if __name__ == "__main__":
    main()
