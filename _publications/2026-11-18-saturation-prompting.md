---
title: "Saturation Prompting: Recovering Stable Categories from Open-Ended Survey Responses with Repeated LLM Extraction"
collection: publications
type: preprint
permalink: /publication/2026-11-18-saturation-prompting
excerpt: 'Saturation prompting repeats LLM category extraction on random samples of open-ended survey responses and counts how often each theme recurs; on four UC Berkeley Social Networks Study questions it recovers more of hand-built codebooks than a single call and makes extraction more reproducible.'
date: 2026-11-18
venue: 'SocArXiv'
paperurl: 'https://osf.io/preprints/socarxiv/wtkpm_v1'
citation: 'Soria C. Saturation Prompting: Recovering Stable Categories from Open-Ended Survey Responses with Repeated LLM Extraction. SocArXiv. 2026. https://osf.io/preprints/socarxiv/wtkpm_v1'
---
A single large language model (LLM) call cannot reliably find the categories in open-ended survey responses because the model samples from a probability distribution and returns different themes each run, so one list cannot tell which belong to the data and which to that draw. The pipeline documented here improves reliability and reproducibility through saturation prompting, in which many independent calls each read a fresh random sample. It counts how often each theme is found and gives a distribution rather than a flat list. For researchers who want a shorter list, the pipeline can also merge labels with the same meaning into a final scheme of distinct categories.

To test the pipeline, I apply saturation prompting to four open-ended survey questions from the UC Berkeley Social Networks Study and compare the results with a single call to the same model. Against the study’s existing codebooks, built by hand and independently, Llama 3.1 8B saturation runs recover 43 to 47 of their 50 categories, against 31 to 37 for its single calls, with the gain on the two more interpretive questions; on the two concrete questions a single call already finds most of them. On a more capable model, Claude Sonnet 5, saturation prompting adds less than it does for Llama over a single prompt asking the model to extract as many categories as it can find. Still, for both models and on every question, saturation finds more distinct categories than a single call. Llama’s additions include whole broad categories, while Sonnet’s are mostly more nuanced distinctions within broad categories its single call already finds. Saturation prompting makes a lower-tier open-weight model that can run on a laptop more reproducible by reducing run-to-run variability. Averaged across the four questions, the similarity between two runs’ ten most frequent labels rises from 0.85 for a single call to 0.96 with 64 calls (1.0 = identical meaning). Merging, although convenient, keeps only 33 to 91 percent of the distinct categories a saturation run finds.

*Revise and resubmit at Survey Practice.*

[Download paper here](https://osf.io/preprints/socarxiv/wtkpm_v1)

Soria C. Saturation Prompting: Recovering Stable Categories from Open-Ended Survey Responses with Repeated LLM Extraction. SocArXiv. 2026. https://osf.io/preprints/socarxiv/wtkpm_v1
