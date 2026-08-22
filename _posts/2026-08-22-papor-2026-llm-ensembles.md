---
title: 'Presenting LLM Ensembles at PAPOR'
date: 2026-08-22
permalink: /posts/2026/08/papor-2026-llm-ensembles/
header:
  og_image: catllm_ensemble.png
tags:
  - CatLLM
  - Large Language Models
  - Survey Research
  - Conferences
---

![CatLLM ensemble of multiple LLM providers](/images/catllm_ensemble.png)

On August 21 I presented "Using LLM Ensembles to Improve Classification of Open-Ended Survey Responses" at the [Pacific Chapter of AAPOR (PAPOR)](https://www.papor.org/), hosted by [KFF](https://www.kff.org/). It was a pleasure to present alongside Kevin Collins of [Survey 160](https://www.survey160.com/), Meredith Massey of the [National Center for Health Statistics](https://www.cdc.gov/nchs/), and Anagha Srivatsav of Miravoice. The full abstract is on the [talk page](/talks/2026-08-21-talk-20).

The short version: large language models are increasingly used to code open-ended survey responses, but they systematically over-classify, assigning categories too liberally on ambiguous cases and producing high sensitivity with low precision. Survey methodologists have long known that aggregating multiple noisy annotators beats any single annotator, so the talk asked whether the same principle transfers to LLMs. Across four open-ended survey questions with human-coded ground truth (3,208 responses) and 16 models spanning three cost tiers and six providers, unanimous voting across models corrects the problem directly: on the most ambiguous categories, the false positive rate drops from 50% to 3% and precision triples. The benefit concentrates exactly where over-classification is worst, on subjectively ambiguous categories with fuzzy boundaries, and it replicates across three independent datasets.

The part I most wanted a room of survey researchers to hear is what drives the correction. It is decorrelated errors, and the most reliable way to get them is cross-provider diversity: models from different providers err differently on ambiguous cases, and consensus filters out the idiosyncratic false positives. Temperature variation and scaling up within a single model family do not reliably do the same. As few as three diverse lower-tier models are enough to beat GPT-5. If you only take one thing from the talk, it is that investing in a few different models is more effective than investing in one expensive model.

The work is written up in [Model Diversity Over Model Size](/publication/2026-06-04-llm-ensembles-survey-coding) (preprint on [SocArXiv](https://osf.io/preprints/socarxiv/er6mz_v1), currently revise and resubmit at *Public Opinion Quarterly*), and unanimous multi-model ensembling ships as a default in [CatLLM](https://github.com/chrissoria/cat-llm).

Thank you to the PAPOR organizers and to KFF for hosting. It was a great group to be in conversation with, and I hope to be back.
