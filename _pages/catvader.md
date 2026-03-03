---
permalink: /catvader/
title: "CatVader"
description: "CatVader - Open-source Python package for classifying and analyzing social media posts using large language models. Connects directly to the Threads API."
author_profile: true
---

## Python Package

<a href="https://pypi.org/project/cat-vader/">Classify and Analyze Social Media Posts</a>: CatVader is a fork of <a href="/catllm/">CatLLM</a> adapted for social media data. It connects directly to the Threads API to pull your post history, classify posts into custom categories using large language models, and return an enriched dataset with engagement metrics — in a few lines of code. <a href="https://github.com/chrissoria/cat-vader">[GitHub]</a>

<a href="https://pepy.tech/projects/cat-vader"><img src="https://static.pepy.tech/badge/cat-vader/month" alt="Downloads per month"></a> <a href="https://pepy.tech/projects/cat-vader"><img src="https://static.pepy.tech/badge/cat-vader" alt="Total Downloads"></a>

## What You Can Do With It

- **Pull your Threads history** — authenticate once and retrieve your full post archive with engagement metrics (likes, views, replies, reposts, shares)
- **Discover categories automatically** — use `explore()` to let the LLM extract recurring themes from your posts before you define any labels
- **Classify at scale** — run `classify()` to assign multi-label categories to every post using any supported LLM provider
- **Extract structured fields** — use `extract()` to pull named entities, claims, or any custom field out of free text
- **Analyze engagement** — the output dataset is ready for downstream analysis: topic distributions, regression models, timing patterns

## Example

```python
import catvader as cv

# Pull and classify the last 12 months of your Threads history
results = cv.classify(
    sm_source="threads",
    sm_months=12,
    categories=[
        "Politics: Posts about political parties, elections, or political figures",
        "Technology: Posts about software, hardware, or the tech industry",
        "Personal: Opinions, reflections, or experiences about everyday life",
    ],
    api_key="your-openai-api-key",
)
```

## Blog Post

For a full end-to-end walkthrough — pulling 850 posts, discovering categories with `explore()`, classifying with Llama 3.3 70B, and running regression models on engagement — see: [Analyzing My Threads Feed with cat-vader](/posts/2026/03/catvader-threads-analysis/)
