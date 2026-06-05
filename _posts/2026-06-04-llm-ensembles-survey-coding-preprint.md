---
title: 'New Preprint: Model Diversity Over Model Size — Unanimous LLM Ensembles Correct Over-Classification in Survey Coding'
date: 2026-06-04
permalink: /posts/2026/06/llm-ensembles-survey-coding-preprint/
tags:
  - Large Language Models
  - Survey Data
  - Categorization
  - Ensembles
  - Unanimous Voting
  - Preprint
---

I have a new preprint out on SocArXiv: [Model Diversity Over Model Size: Unanimous LLM Ensembles Correct Over-Classification in Survey Coding](https://osf.io/preprints/socarxiv/er6mz_v1). It's a deep dive into one finding flagged in the [CatLLM methods paper](https://osf.io/preprints/socarxiv/gjvcf_v1) — that unanimous multi-model ensembling corrects over-classification — asking *which* ensemble ingredients actually drive the gain and *where* the gain shows up.

## Abstract

Large language models are increasingly used to classify open-ended survey responses, but they systematically over-classify, assigning categories too liberally on ambiguous cases and producing high sensitivity but low precision. Drawing on the established principle that aggregating multiple noisy annotators outperforms any single annotator, we test whether ensembles of LLMs can correct this problem. Using four open-ended survey questions with human-coded ground truth (3,208 responses, 6 categories per question), we evaluate ensemble configurations across 16 models spanning three cost tiers and six providers.

## Key Findings

- **Unanimous voting fixes the over-classification problem.** On the most ambiguous categories, the false positive rate drops from 50% to 3% under unanimous agreement, and precision triples.
- **The gain concentrates where over-classification is worst.** Subjectively ambiguous categories with fuzzy boundaries see large improvements; categories with clear criteria show no benefit. The pattern replicates across three independent datasets (UCNets, GoEmotions, the British Election Study).
- **Cross-provider model diversity is the active ingredient.** Models from different providers make different errors on ambiguous cases, and consensus filters the idiosyncratic false positives. Temperature variation and within-family size scaling contribute essentially nothing.
- **Three cheap models can beat one expensive one.** As few as three diverse lower-tier models suffice to reliably exceed GPT-5 on the ambiguous classification tasks where this matters most.

## Implications

For the ambiguous classification problems common in open-ended survey research, the well-established annotation principle of multi-coder agreement transfers directly to LLMs: investing in *diverse perspectives* is more effective than investing in a single expensive model. Practically, this means survey researchers can often skip the frontier-tier subscription and instead orchestrate a small cross-provider ensemble — frequently at a fraction of the cost.

[Read the full preprint on SocArXiv](https://osf.io/preprints/socarxiv/er6mz_v1) · [Replication materials](https://anonymous.4open.science/r/catllm-replication-A4E2/README.md) · [CatLLM (the toolkit used to produce the classifications)](https://catllm.com)
