---
permalink: /catllm/
title: "CatLLM"
description: "CatLLM - Open-source Python and R ecosystem for LLM-powered text classification: survey responses, social media, academic papers, political text, web content, images, and PDFs. Built for social science researchers."
author_profile: true
---

<div style="padding: 14px 18px; margin-bottom: 28px; background: #f4f9f8; border-left: 3px solid #2a9d8f; border-radius: 4px; font-size: 0.95rem;">
  <strong>Project site:</strong> <a href="https://catllm.com">catllm.com</a> — the full project landing page with documentation, examples, and citation info.
</div>

## Overview

**CatLLM** is an open-source Python and R ecosystem for systematic LLM-powered text classification. The `cat-llm` meta-package installs a family of domain-specific tools — survey responses, social media, academic papers, political text, web content, and more — all sharing the same `classify()` / `extract()` / `summarize()` API. Validated against expert human coders across multiple datasets.

<a href="https://pypi.org/project/cat-llm/"><img src="https://static.pepy.tech/badge/cat-llm/month" alt="Downloads per month"></a> <a href="https://pypi.org/project/cat-llm/"><img src="https://static.pepy.tech/badge/cat-llm" alt="Total Downloads"></a> <a href="https://doi.org/10.21105/joss.09678"><img src="https://joss.theoj.org/papers/10.21105/joss.09678/status.svg" alt="JOSS DOI"></a>

## The Ecosystem

### Meta-package

<a href="https://pypi.org/project/cat-llm/">cat-llm</a>: The full ecosystem in one install (`pip install cat-llm`). Provides every domain package through a single `import catllm` namespace. <a href="https://github.com/chrissoria/cat-llm">[GitHub]</a>

### General-purpose base

<a href="https://pypi.org/project/cat-stack/">cat-stack</a>: The domain-agnostic classification engine underlying every other package. Use it directly for general text, or build your own domain wrapper on top of it. <a href="https://github.com/chrissoria/cat-stack">[GitHub]</a>

<a href="https://pepy.tech/projects/cat-stack"><img src="https://static.pepy.tech/badge/cat-stack/month" alt="Downloads per month"></a> <a href="https://pepy.tech/projects/cat-stack"><img src="https://static.pepy.tech/badge/cat-stack" alt="Total Downloads"></a>

### Domain packages

<a href="https://pypi.org/project/cat-survey/">cat-survey</a>: Classify open-ended **survey responses** at scale. Verbose category definitions and ensemble voting handle ambiguity. <a href="https://github.com/chrissoria/cat-survey">[GitHub]</a>

<a href="https://pepy.tech/projects/cat-survey"><img src="https://static.pepy.tech/badge/cat-survey/month" alt="Downloads per month"></a> <a href="https://pepy.tech/projects/cat-survey"><img src="https://static.pepy.tech/badge/cat-survey" alt="Total Downloads"></a>

<a href="https://pypi.org/project/cat-pol/">cat-pol</a>: Classify **political text** — municipal ordinances, federal laws, executive orders, presidential speeches. Ships with 17 built-in datasets on HuggingFace, updated weekly. <a href="https://github.com/chrissoria/cat-pol">[GitHub]</a>

<a href="https://pepy.tech/projects/cat-pol"><img src="https://static.pepy.tech/badge/cat-pol/month" alt="Downloads per month"></a> <a href="https://pepy.tech/projects/cat-pol"><img src="https://static.pepy.tech/badge/cat-pol" alt="Total Downloads"></a>

<a href="https://pypi.org/project/cat-vader/">cat-vader</a>: Classify and analyze **social media posts**. Connects to the Threads API to pull your full post history, classify posts into custom categories, and return an enriched dataset with engagement metrics. <a href="/catvader/">[Learn more]</a> <a href="https://github.com/chrissoria/cat-vader">[GitHub]</a>

<a href="https://pepy.tech/projects/cat-vader"><img src="https://static.pepy.tech/badge/cat-vader/month" alt="Downloads per month"></a> <a href="https://pepy.tech/projects/cat-vader"><img src="https://static.pepy.tech/badge/cat-vader" alt="Total Downloads"></a>

<a href="https://pypi.org/project/cat-ademic/">cat-ademic</a>: Classify and summarize **academic papers** — abstracts, full texts, and research documents across disciplines. Built-in journal/field context. <a href="https://github.com/chrissoria/cat-ademic">[GitHub]</a>

<a href="https://pepy.tech/projects/cat-ademic"><img src="https://static.pepy.tech/badge/cat-ademic/month" alt="Downloads per month"></a> <a href="https://pepy.tech/projects/cat-ademic"><img src="https://static.pepy.tech/badge/cat-ademic" alt="Total Downloads"></a>

<a href="https://pypi.org/project/cat-cog/">cat-cog</a>: **Cognitive assessment** scoring, including CERAD Constructional Praxis test evaluation for dementia research. <a href="https://github.com/chrissoria/cat-cog">[GitHub]</a>

<a href="https://pepy.tech/projects/cat-cog"><img src="https://static.pepy.tech/badge/cat-cog/month" alt="Downloads per month"></a> <a href="https://pepy.tech/projects/cat-cog"><img src="https://static.pepy.tech/badge/cat-cog" alt="Total Downloads"></a>

<a href="https://pypi.org/project/cat-web/">cat-web</a>: Classify scraped **web content** — pages, articles, and HTML. Domain-tuned prompts for long-form online text. <a href="https://github.com/chrissoria/cat-web">[GitHub]</a>

<a href="https://pepy.tech/projects/cat-web"><img src="https://static.pepy.tech/badge/cat-web/month" alt="Downloads per month"></a> <a href="https://pepy.tech/projects/cat-web"><img src="https://static.pepy.tech/badge/cat-web" alt="Total Downloads"></a>

## Apps

<a href="https://catllm.com#download">CatLLM Desktop (Mac)</a>: A self-contained Mac app — drag in a CSV, pick categories, get a coded dataset back. Same engine as the Python and R packages, no Python install required.

<a href="https://huggingface.co/spaces/CatLLM/survey-classifier">Classify Survey Responses</a>: A web-based tool for categorizing survey responses without writing code.

## Citation

If you use CatLLM in your research, please cite:

Soria, C. (2026). *Scaling Open-Ended Survey Coding: An LLM Pipeline Where Definitions Do the Heavy Lifting*. *Journal of Open Source Software*. <a href="https://doi.org/10.21105/joss.09678">https://doi.org/10.21105/joss.09678</a>
