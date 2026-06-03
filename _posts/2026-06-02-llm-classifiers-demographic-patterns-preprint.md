---
title: 'New Preprint: High Agreement, Different Stories — How LLM Classifiers Reshape Demographic Patterns in Survey Data'
date: 2026-06-02
permalink: /posts/2026/06/llm-classifiers-demographic-patterns-preprint/
tags:
  - Large Language Models
  - Survey Data
  - Categorization
  - Demographic Patterns
  - Preprint
---

I have a new preprint out on SocArXiv: [High Agreement, Different Stories: How LLM Classifiers Reshape Demographic Patterns in Survey Data](https://osf.io/preprints/socarxiv/85kyd_v1). This is a substantially revised version of my earlier preprint, with new analyses centered on how high agreement rates can mask thematic and demographic divergence between LLM and human coders.

## Abstract

What we learn from open-ended survey data depends on who—or what—does the coding. Large Language Models (LLMs) promise to democratize qualitative analysis, but do high agreement rates translate into equivalent thematic findings? This study compares eight LLMs to human annotators on a multilabel coding task using 3,200 responses from the UC Berkeley Social Networks Study, comprising over 19,000 coding decisions. Although LLM-human reliability does not match human-human reliability overall, LLMs approach human performance on simpler tasks and can serve as useful additional coders for generating consensus labels.

## Key Findings

- Compared to a gold-standard human consensus, models achieve 82–97% per-category agreement, but macro F1 is lower and response-level similarity is lower still: even the best model reproduces the full human label set for fewer than 60% of responses.
- High agreement masks thematic divergence. Models systematically over-identify themes, assigning 67% more categories per response, especially for categories requiring greater interpretive judgment.
- Models show lower agreement for some demographic groups. These gaps are partly explained by response characteristics such as length, clarity, and atypicality, and some persist after controls, with implications for studies of populations whose response styles diverge from the corpus average.
- At the sample level, models largely preserve the overall thematic narrative: human and model category rankings correlate strongly (pooled Spearman's ρ = 0.75), and top-performing models achieve approximately 80% directional agreement on demographic patterns.
- Concrete behavioral questions—such as reasons for moving or strategies for making friends—show especially strong alignment, whereas more interpretive questions show greater divergence.

## Implications

Systematic over-classification can still shift narratives about how specific groups behave, leading researchers to report patterns that the human gold standard does not support. LLMs can meaningfully reduce coding burden, but for studies sensitive to demographic nuance they are best treated as additional coders contributing to a human-anchored consensus rather than as drop-in replacements.

[Read the full preprint on SocArXiv](https://osf.io/preprints/socarxiv/85kyd_v1) · [Project page and code on OSF](https://osf.io/nqep5/)
