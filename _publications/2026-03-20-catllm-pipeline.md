---
title: "Scaling Open-Ended Survey Coding: An LLM Pipeline Where Definitions Do the Heavy Lifting"
collection: publications
type: preprint
permalink: /publication/2026-03-20-catllm-pipeline
excerpt: 'CatLLM is an open-source Python and R package offering a three-stage pipeline for coding open-ended survey responses with large language models, with defaults calibrated by a systematic empirical study evaluating 21 LLMs across three capability tiers, six providers, and four survey questions.'
date: 2026-03-20
venue: 'SocArXiv'
paperurl: 'https://osf.io/preprints/socarxiv/gjvcf_v1'
citation: 'Soria C. Scaling Open-Ended Survey Coding: An LLM Pipeline Where Definitions Do the Heavy Lifting. SocArXiv. 2026. https://osf.io/preprints/socarxiv/gjvcf_v1'
---
As large language model (LLM)–based text classification becomes routine in the social sciences, researchers confront dozens of competing models, inconsistent advice on prompting, and little standardized tooling with evidence-based defaults. CatLLM, an open-source Python and R package, addresses this gap with a three-stage pipeline—exploration, extraction, classification—for coding open-ended survey responses. The package offers a provider-agnostic interface that supports multi-model ensembles, batch processing, and fully local deployment via open-weight models, and can be operated through a conversational interface by researchers with no programming experience. CatLLM's defaults are calibrated by a systematic empirical study evaluating 21 LLMs across three capability tiers, six providers, and four survey questions, benchmarked against sociologist-coded ground truth. This validation reveals a consistent problem: all models over-classify, with precision lagging 40–50 percentage points behind sensitivity, implying that default LLM configurations may substantially overstate category prevalence. CatLLM encodes empirically grounded mitigations as defaults: verbose category definitions with explicit inclusion and exclusion criteria, unanimous multi-model ensembling, and an automatic "Other" escape-valve category, while disabling advanced prompting strategies that show no reliable benefit. Ensembles of inexpensive open-weight models outperform the best individual cloud model, enabling fully local deployment without transmitting survey data to external servers. These findings replicate on two independent public datasets spanning political and emotional text, and an applied example linking tool-coded "move reasons" to respondent demographics uncovers distinct life-course patterns in residential mobility.

*Under review at the Journal of Computational Social Science.*

[Download paper here](https://osf.io/preprints/socarxiv/gjvcf_v1)

Soria C. Scaling Open-Ended Survey Coding: An LLM Pipeline Where Definitions Do the Heavy Lifting. SocArXiv. 2026. https://osf.io/preprints/socarxiv/gjvcf_v1
