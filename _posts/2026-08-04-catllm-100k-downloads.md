---
title: '100,000 Downloads: What CatLLM Has Built So Far'
date: 2026-08-04
permalink: /posts/2026/08/catllm-100k-downloads/
description: 'CatLLM has passed 100,000 downloads on PyPI. A look at the peer-reviewed validation behind its defaults, the papers it has produced, and the non-survey research people are using it for.'
header:
  og_image: wide_cat_llm.png
tags:
  - CatLLM
  - Large Language Models
  - Text Classification
  - Survey Research
  - Open Source
  - Reproducibility
  - Computational Social Science
---

![CatLLM logo](/images/wide_cat_llm.png)

[CatLLM](https://pypi.org/project/cat-llm/) has passed **100,000 downloads on PyPI**. I started it because I had a column of open-ended survey responses and no good way to code them at scale; I did not expect it to end up anywhere near six figures.

I want to mark the number, but the number is not really the interesting part. Downloads measure adoption, not whether a tool is any good. So this post is about the two things I think actually matter: what the defaults are grounded in, and what people have built with it.

## The Defaults Are Empirical Claims, Not Preferences

Most LLM classification tooling ships with defaults chosen because they seemed reasonable. CatLLM's defaults are the output of benchmarking studies against human-coded ground truth, and every one of them exists because the alternative measurably failed.

The core finding across those studies is that **LLMs systematically over-classify.** They assign categories too liberally on ambiguous cases, producing high sensitivity and much lower precision, which means default configurations can substantially overstate how common a theme is in your data. That single failure mode is what most of CatLLM's defaults are designed to correct:

- **Verbose category definitions with explicit inclusion and exclusion criteria.** Vague category labels are where over-classification concentrates.
- **Unanimous multi-model ensembling.** Requiring cross-provider agreement drops the false positive rate on the most ambiguous categories from 50% to 3% and triples precision.
- **An automatic "Other" escape valve.** Models forced to choose among your categories will force-fit responses that belong in none of them.
- **Advanced prompting strategies off by default.** They showed no reliable benefit on these tasks, so they are opt-in rather than assumed.

The package is also peer-reviewed. It went through review at the *Journal of Open Source Software*, and the empirical validation behind the defaults is written up separately and under review at disciplinary journals. That is a deliberately slower path than shipping a package and writing a README, and I think it is the right one for tooling that produces variables people then run regressions on.

## The Papers

Five papers so far, all of which either document CatLLM or exist because of the validation work behind it. All preprints are open access.

**Peer-reviewed:**

- Soria C. [CatLLM: A Python package for Generating, Assigning, and Scoring Open-Ended Survey Data and Images](https://doi.org/10.21105/joss.09678). *Journal of Open Source Software.* 2026. doi:10.21105/joss.09678

**Preprints under review:**

- Soria C. [Scaling Open-Ended Survey Coding: An LLM Pipeline Where Definitions Do the Heavy Lifting](https://osf.io/preprints/socarxiv/gjvcf_v1). *SocArXiv.* 2026.
  <br>*21 LLMs, three capability tiers, six providers, four survey questions, benchmarked against sociologist-coded ground truth. This is the study the defaults come from. Under review at the Journal of Computational Social Science.*

- Soria C. [High Agreement, Different Stories: How LLM Classifiers Reshape Demographic Patterns in Survey Data](https://osf.io/preprints/socarxiv/85kyd_v1). *SocArXiv.* 2026.
  <br>*Eight LLMs against human annotators on 3,200 responses and over 19,000 coding decisions. Models hit 82–97% per-category agreement while reproducing the full human label set for fewer than 60% of responses, and the gap is not evenly distributed across demographic groups. Revise and resubmit at the Journal of Survey Statistics and Methodology.*

- Soria C. [Model Diversity Over Model Size: Unanimous LLM Ensembles Correct Over-Classification in Survey Coding](https://osf.io/preprints/socarxiv/er6mz_v1). *SocArXiv.* 2026.
  <br>*Sixteen models across three cost tiers and six providers. Cross-provider diversity is the active ingredient, not model size or temperature; three diverse cheap models reliably beat GPT-5. Revise and resubmit at Public Opinion Quarterly.*

- Soria C. [What Does Frontier Access Buy? Benchmarking LLM Access Tiers and the Reproducibility Case for Open Weights in Survey Coding](https://osf.io/preprints/socarxiv/5g34x_v1). *SocArXiv.* 2026.
  <br>*Eighteen LLMs across four access tiers on five tasks. The flagship tier's accuracy margin over cheaper models is statistically indistinguishable from zero despite costing 1.3–6× more per token, and the largest open-weight models match both proprietary tiers on cell-level agreement. Under review at Social Science Computer Review.*

The practical upshot of the last two, if you only take one thing from this section: you probably do not need the expensive model. You need a few different ones.

## It Stopped Being a Survey Tool

I built CatLLM for open-ended survey responses. That is still the use case I understand best and the one the validation studies target. But the same three-stage pipeline (explore, extract, classify) turns out to be indifferent to where the text came from, and people have taken it well outside survey methodology.

Some of what it is being used for now:

- **Local policy.** Municipal ordinances are dense, high-volume, and almost entirely unanalyzed. I used the pipeline to classify 200 recent ordinances each from San Diego and San Francisco against a policy taxonomy and a political lean scheme; you can read [what came out of that](/posts/2026/03/catpol-ordinance-analysis/).
- **Social media.** People are coding their own posting histories and public platform data. I wrote up analyses of [Bluesky](/posts/2026/03/catvader-bluesky-analysis/) and [Threads](/posts/2026/03/catvader-threads-analysis/) content using the same machinery.
- **Academic literature.** Screening and coding papers at a volume that makes manual abstract review impractical.
- **Documents and images.** PDF and image classification for anything that lives in a scanned archive rather than a clean CSV.

That range is why the ecosystem split into domain packages (`cat-pol` for political text, `cat-vader` for social media, `cat-ademic` for academic writing, `cat-web`, `cat-cog`, `cat-survey`) on a shared `cat-stack` engine. It is also available [in R](/posts/2026/05/cat-llm-r-packages/), in Stata, as a [Mac desktop app](/posts/2026/05/catllm-mac-desktop-app/), as a [web app](/posts/2026/01/catllm-web-app/), and [through Claude Code](/posts/2026/03/catllm-claude-code/) for researchers who would rather not write any code at all.

## If You've Used It, I'd Like to Know

Here is the actual ask.

PyPI tells me the package has been downloaded. It tells me nothing about who, for what, or whether the results held up. I have no way to find the work CatLLM has contributed to unless someone tells me about it.

**If you have used CatLLM in a paper, a preprint, a thesis, a dissertation, a class assignment, a report, or a blog post, I would genuinely like to hear about it.** I want to maintain a public list of work that used the package, and I want to know which parts held up under conditions I never tested. I am especially interested in:

- Non-English text and non-U.S. contexts, which the validation studies barely cover.
- Domains I have not benchmarked at all: clinical notes, interview transcripts, historical documents, customer feedback.
- Cases where it did *not* work. Negative results are more useful to me than success stories, and they will shape the defaults for the next version.

Reach me at **chrissoria@berkeley.edu**, or open a thread on the [GitHub repo](https://github.com/chrissoria/cat-llm). No formality needed. A link and a sentence is plenty.

## Install It

```bash
pip install cat-llm
```

Everything is open source under GPL-3.0 and it will stay that way. The full pipeline runs on free HuggingFace models or locally through [Ollama](https://ollama.com) at zero API cost, and, per the access-tier study, local open-weight models are a real option rather than a consolation prize. There is no paid tier and there is not going to be one.

If you use it in published work, the citation is:

> Soria C. CatLLM: A Python package for Generating, Assigning, and Scoring Open-Ended Survey Data and Images. *Journal of Open Source Software.* 2026. doi:[10.21105/joss.09678](https://doi.org/10.21105/joss.09678)

Thanks to everyone who filed an issue, reported a bug, or asked for a provider I had not added yet. A hundred thousand downloads is a nice round number, but the issues are what actually made the package better.
