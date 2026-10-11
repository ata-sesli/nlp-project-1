"""Build the benchmark from the predictions of every model.

Reads benchmark/predictions/<model>/<split>.csv (id, label, p_deny) and latency.json, scores
every model with the same function (distilbert/evaluate_predictions.py: metrics) and writes to
benchmark/results/:
    benchmark.csv            one row per model and split
    benchmark_by_group.csv   the test split by difficulty and by call_has_both_labels
    benchmark.md             the same tables, readable
    *.png                    the charts

    python benchmark/run_benchmark.py

Models with no predictions yet are skipped. Needs no model files and no GPU.
"""

import argparse
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import MODELS, PRED, ROOT, SPLITS, load_split, model_info

sys.path.insert(0, os.path.join(ROOT, "distilbert"))
from evaluate_predictions import metrics  # noqa: E402  (one metric function for every model)

OUT = os.path.join(ROOT, "benchmark", "results")
GROUPS = ["difficulty", "call_has_both_labels"]
KEYS = ["rows", "macro_f1", "accuracy", "false_allow_rate", "false_deny_rate", "auroc"]
DIFFICULTIES = ["easy", "medium", "hard"]

SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#898781", "#e6e5e0"
INPUT_COLOR = {"A": "#2a78d6", "B": "#eb6834"}
INPUT_LABEL = {"A": "A: tool call only", "B": "B: call + request + history"}


def collect(threshold):
    names = [m for m in MODELS if os.path.isdir(os.path.join(PRED, m))]
    names += sorted(m for m in os.listdir(PRED) if m not in MODELS and os.path.isdir(os.path.join(PRED, m)))
    meta, rows, groups = {}, [], []
    for name in names:
        arch, specific, col, role = model_info(name)
        ident = {"model": name, "architecture": arch, "specific_model": specific,
                 "input": col[-1].upper(), "role": role}
        latency = {}
        if os.path.exists(os.path.join(PRED, name, "latency.json")):
            with open(os.path.join(PRED, name, "latency.json")) as f:
                latency = json.load(f)
        for split in SPLITS:
            path = os.path.join(PRED, name, f"{split}.csv")
            if not os.path.exists(path):
                continue
            if split not in meta:
                meta[split] = load_split(split, ["id"] + GROUPS)
            df = pd.read_csv(path).merge(meta[split], on="id", how="left", validate="one_to_one")
            m = metrics(df["label"].to_numpy(), df["p_deny"].to_numpy(), threshold)
            rows.append({**ident, "split": split, **{k: m[k] for k in KEYS}, **m["confusion"],
                         "latency_ms_p50": latency.get("ms_p50"), "latency_ms_p95": latency.get("ms_p95")})
            if split != "test":
                continue
            for g in GROUPS:
                for value, sub in df.groupby(g):
                    gm = metrics(sub["label"].to_numpy(), sub["p_deny"].to_numpy(), threshold)
                    groups.append({**ident, "group": g, "value": str(value), **{k: gm[k] for k in KEYS}})
    return pd.DataFrame(rows), pd.DataFrame(groups)


def write_markdown(bench, groups, threshold):
    def table(df, first):
        cols = first + KEYS + [c for c in ["latency_ms_p50"] if c in df]
        lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(first) + "---:|" * (len(cols) - len(first))]
        for _, r in df.iterrows():
            cells = [str(r[c]) if c in first or c == "rows" else ("-" if pd.isna(r[c]) else f"{r[c]:.4f}")
                     for c in cols]
            lines.append("| " + " | ".join(cells) + " |")
        return lines

    lines = [f"# Benchmark (deny when p_deny >= {threshold})", ""]
    for split in SPLITS:
        part = bench[bench["split"] == split]
        if len(part):
            lines += [f"## {split}", ""] + table(part, ["model", "input"]) + [""]
    for g in GROUPS:
        part = groups[groups["group"] == g] if len(groups) else groups
        if len(part):
            lines += [f"## test, by {g}", ""] + table(part, ["model", "input", "value"]) + [""]
    with open(os.path.join(OUT, "benchmark.md"), "w") as f:
        f.write("\n".join(lines))


def style(ax, grid="y"):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, length=0, labelsize=9)
    if grid:
        ax.grid(axis=grid, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def chart_a_vs_b(test, key, title, name):
    """One group of bars per architecture: input A next to input B."""
    archs = list(dict.fromkeys(test["architecture"]))
    fig, ax = plt.subplots(figsize=(1.6 + 1.9 * len(archs), 4), facecolor=SURFACE)
    width = 0.36
    top = 1.08 if key == "macro_f1" else max(test[key].max() * 1.25, 0.01)
    for i, inp in enumerate(["A", "B"]):
        part = test[test["input"] == inp].set_index("architecture")
        xs = [archs.index(a) + (i - 0.5) * (width + 0.03) for a in part.index]
        ax.bar(xs, part[key], width, color=INPUT_COLOR[inp], label=INPUT_LABEL[inp])
        for x, v in zip(xs, part[key]):
            ax.text(x, v + top * 0.012, f"{v:.3f}", ha="center", va="bottom", fontsize=9, color=INK)
    ax.set_xticks(range(len(archs)), archs)
    ax.tick_params(axis="x", labelcolor=INK)
    ax.set_ylim(0, top)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=28)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=9, labelcolor=INK)
    style(ax)
    save(fig, name)


def chart_latency(test):
    """Macro-F1 against CPU time per row; every point is labelled with its model."""
    part = test.dropna(subset=["latency_ms_p50"])
    if part.empty:
        return
    fig, ax = plt.subplots(figsize=(7, 4.2), facecolor=SURFACE)
    for inp in ["A", "B"]:
        sub = part[part["input"] == inp]
        ax.scatter(sub["latency_ms_p50"], sub["macro_f1"], s=70, color=INPUT_COLOR[inp], edgecolor=SURFACE,
                   linewidth=2, label=INPUT_LABEL[inp], zorder=3)
    for _, r in part.iterrows():
        ax.annotate(r["architecture"], (r["latency_ms_p50"], r["macro_f1"]), xytext=(8, 6),
                    textcoords="offset points", fontsize=9, color=INK)
    ax.set_xscale("log")
    ax.set_xlabel("CPU time per row, median, ms (log scale)", color=MUTED, fontsize=9)
    ax.set_ylabel("macro-F1 on the test split", color=MUTED, fontsize=9)
    ax.set_title("Accuracy against speed", loc="left", fontsize=11, color=INK, pad=28)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=9, labelcolor=INK)
    style(ax, grid="both")
    save(fig, "f1_vs_latency.png")


def chart_difficulty(groups):
    """One small panel per model: macro-F1 on easy, medium and hard test rows."""
    part = groups[groups["group"] == "difficulty"] if len(groups) else groups
    part = part[part["value"].isin(DIFFICULTIES)] if len(part) else part
    names = list(dict.fromkeys(part["model"])) if len(part) else []
    if not names:
        return
    fig, axes = plt.subplots(1, len(names), figsize=(2.6 * len(names), 3.6), sharey=True, facecolor=SURFACE,
                             squeeze=False)
    for ax, name in zip(axes[0], names):
        sub = part[part["model"] == name].set_index("value").reindex(DIFFICULTIES)
        inp = sub["input"].dropna().iloc[0]
        ax.bar(DIFFICULTIES, sub["macro_f1"], 0.6, color=INPUT_COLOR[inp])
        for x, v in enumerate(sub["macro_f1"]):
            if not pd.isna(v):
                ax.text(x, v + 0.012, f"{v:.3f}", ha="center", va="bottom", fontsize=8, color=INK)
        ax.set_title(f"{sub['architecture'].dropna().iloc[0]}\ninput {inp}", fontsize=9, color=INK)
        ax.set_ylim(0, 1.08)
        ax.tick_params(axis="x", labelcolor=INK)
        style(ax)
    fig.suptitle("Macro-F1 on the test split, by difficulty", x=0.02, ha="left", fontsize=11, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    save(fig, "f1_by_difficulty.png")


def chart_confusion(test):
    """One confusion matrix per model on the test split, as shares of each true class."""
    n = len(test)
    cols = min(n, 4)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(2.7 * cols, 2.9 * rows), facecolor=SURFACE, squeeze=False)
    for ax in axes.flat:
        ax.axis("off")
    for ax, (_, r) in zip(axes.flat, test.iterrows()):
        ax.axis("on")
        m = np.array([[r["tn"], r["fp"]], [r["fn"], r["tp"]]], dtype=float)
        share = m / m.sum(axis=1, keepdims=True).clip(min=1)
        ax.imshow(share, cmap="Blues", vmin=0, vmax=1)
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{int(m[i, j]):,}\n{share[i, j]:.1%}", ha="center", va="center", fontsize=8,
                        color="white" if share[i, j] > 0.5 else INK)
        ax.set_xticks([0, 1], ["allow", "deny"])
        ax.set_yticks([0, 1], ["allow", "deny"])
        ax.set_xlabel("predicted", fontsize=8, color=MUTED)
        ax.set_ylabel("true", fontsize=8, color=MUTED)
        ax.set_title(f"{r['architecture']}\ninput {r['input']}", fontsize=9, color=INK)
        ax.tick_params(colors=MUTED, length=0, labelsize=8)
        for side in ax.spines.values():
            side.set_visible(False)
    fig.tight_layout()
    save(fig, "confusion_matrices.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=float, default=0.5, help="deny when p_deny >= threshold")
    a = ap.parse_args()
    if not os.path.isdir(PRED):
        sys.exit(f"no predictions in {PRED}: run the score_*.py scripts first")
    os.makedirs(OUT, exist_ok=True)

    bench, groups = collect(a.threshold)
    if bench.empty:
        sys.exit(f"no predictions in {PRED}: run the score_*.py scripts first")
    bench.to_csv(os.path.join(OUT, "benchmark.csv"), index=False)
    groups.to_csv(os.path.join(OUT, "benchmark_by_group.csv"), index=False)
    write_markdown(bench, groups, a.threshold)

    test = bench[bench["split"] == "test"]
    if len(test):
        chart_a_vs_b(test, "macro_f1", "Macro-F1 on the test split", "f1_a_vs_b.png")
        chart_a_vs_b(test, "false_allow_rate", "False allow rate on the test split (harmful calls let through)",
                     "false_allow_rate.png")
        chart_latency(test)
        chart_difficulty(groups)
        chart_confusion(test)
    print(bench[["model", "split"] + KEYS].to_string(index=False))
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
