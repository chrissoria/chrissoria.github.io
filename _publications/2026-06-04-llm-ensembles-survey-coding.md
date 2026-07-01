---
title: "Model Diversity Over Model Size: Unanimous LLM Ensembles Correct Over-Classification in Survey Coding"
collection: publications
type: preprint
permalink: /publication/2026-06-04-llm-ensembles-survey-coding
excerpt: 'Across 16 LLMs and four open-ended survey questions, unanimous voting across diverse models corrects over-classification on subjectively ambiguous categories, with cross-provider diversity—not temperature or within-family size—as the active ingredient. As few as three diverse lower-tier models can reliably exceed GPT-5.'
date: 2026-06-04
venue: 'SocArXiv'
paperurl: 'https://osf.io/preprints/socarxiv/er6mz_v1'
citation: 'Soria C. Model Diversity Over Model Size: Unanimous LLM Ensembles Correct Over-Classification in Survey Coding. SocArXiv. 2026. https://osf.io/preprints/socarxiv/er6mz_v1'
---
Large language models are increasingly used to classify open-ended survey responses, but they systematically over-classify, assigning categories too liberally on ambiguous cases and producing high sensitivity but low precision. This problem is most severe on subjectively ambiguous categories where models default to "yes" when uncertain. Drawing on the established principle that aggregating multiple noisy annotators outperforms any single annotator, we test whether ensembles of LLMs can correct this problem. Using four open-ended survey questions with human-coded ground truth (3,208 responses, 6 categories per question), we evaluate ensemble configurations across 16 models spanning three cost tiers and six providers. Unanimous voting (requiring all models to agree before assigning a category) directly corrects over-classification by dramatically improving specificity: on the most ambiguous categories, the false positive rate drops from 50% to 3%, and precision triples. This advantage concentrates precisely where over-classification is worst, on subjectively ambiguous categories with fuzzy boundaries, while categories with clear criteria show no benefit. This pattern replicates across three independent datasets. Cross-provider model diversity is the key ingredient: models from different providers make different errors on ambiguous cases, and consensus filters the idiosyncratic false positives. Temperature variation and within-family size scaling contribute nothing. As few as three diverse lower-tier models suffice to reliably exceed GPT-5. For the ambiguous classification problems common in open-ended survey research, the well-established annotation principle of multi-coder agreement transfers directly to LLMs: investing in diverse perspectives is more effective than investing in a single expensive model.

*Revise and resubmit at Public Opinion Quarterly.*
