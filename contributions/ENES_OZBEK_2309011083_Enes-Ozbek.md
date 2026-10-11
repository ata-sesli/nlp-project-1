# Enes Özbek: contribution

**Role:** data preparation. I chose the dataset, built and ran the cleaning pipeline, and
prepared the data for the team. Everything I made is in the `dataset/` folder.

## What I did

1. **Chose the dataset.** I compared candidate datasets for deciding whether an AI agent's
   action should be allowed or denied, and picked
   [ProCreations/auto-1b-data](https://huggingface.co/datasets/ProCreations/auto-1b-data):
   725,000 labeled agent actions, each with the user's request and the agent's earlier steps.
   I kept two other datasets, approve-or-deny and saroku, as outside test sets.
2. **Made the data decisions.** Keep every usable row (no random sampling), keep short, medium
   and long examples so we can measure how input length affects each model, and send commands
   that repeat more than 20 times to training only, so one command cannot decide the test score.
3. **Built the cleaning pipeline** (`dataset/prepare_dataset.py`):
   - English only, checked on the language tag and on the user's request itself: 229,327 rows
     removed.
   - Long-context rows of up to 65,000 tokens removed: 17,077 rows.
   - Exact and near duplicates removed: 8 rows.
   - Split 70/15/15 with seed 42, keeping the label and difficulty mix in each part. All rows
     with the same command stay in the same part, so the test only has commands the model has
     never seen.
   - The outside test sets go through the same steps and lose every command that is also in
     the main data.
   - The output is the same, byte for byte, on every run. `dataset/data/REPORT.md` and
     `dataset/data/stats.json` give the counts after every step, and
     `dataset/data/dropped.jsonl.gz` lists every removed row and why.
4. **Designed the two model inputs** (`dataset/mayi_input.py`): the command alone (`input_a`), and the
   command with the user's request and the agent's history (`input_b`).
5. **Made the build reproducible** in Colab (`dataset/mayi_colab.ipynb`). The raw files are on
   this repo's Releases page (tag `raw-data`) with their checksums.
6. **Wrote the team's external test kit:** `dataset/external_tests/GUIDELINES.md`, the template,
   and `dataset/validate_external_tests.py`, which rejects examples whose command is already in the data.
7. **Analysis for the team:** DistilBERT token lengths for each length bucket (how often the
   512-token limit cuts an example) and the class balance of every split.
8. **Documentation:** `dataset/README.md` and `dataset/DETAILS.md`.

I used Claude, an AI assistant, to help write and check the code. I chose the dataset and made
the decisions above.

## Where my work is

- In this repo: the `dataset/` folder, the raw data release and this file.
- I first built and published the dataset in my own data repo,
  [Enes-Ozbek/LucidAI-Dataset](https://github.com/Enes-Ozbek/LucidAI-Dataset), whose commits show
  each step: the first version, the rebuild that kept every usable row, the rebuilt data and the
  new README.
