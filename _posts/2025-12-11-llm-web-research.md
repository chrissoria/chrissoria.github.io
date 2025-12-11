---
title: 'New Python Package: llm-web-research for Verified Web Research'
date: 2025-12-11
permalink: /posts/2025/12/llm-web-research/
header:
  og_image: logo_llm_researcher.png
tags:
  - Large Language Models
  - Python Package
  - Web Research
  - Data Collection
---

![llm-web-research](/images/logo_llm_researcher.png)

I'm excited to announce the release of a new Python package: [**llm-web-research**](https://github.com/chrissoria/llm-web-research). Part of the [CatLLM](https://pypi.org/project/cat-llm/) ecosystem, this tool enables LLM-powered web research with a focus on accuracy over quantity—designed for researchers who need verified, high-quality data.

## The Problem

When using LLMs for web research, a common issue is ambiguity. Searching for information about "John Smith" or "Springfield" can return incorrect results due to name conflicts and common entities. For research applications where false positives are costly, we need a more rigorous approach.

## The Solution: Multi-Step Verification

The core innovation of llm-web-research is a 4-step verification pipeline that catches ambiguous queries before returning potentially incorrect answers:

1. **Information Gathering** — Initial web search to understand the entity and context
2. **Ambiguity Detection** — Explicit checks for name conflicts, common names, and contradictions
3. **Skeptical Verification** — Secondary search actively looking for contradicting information
4. **Structured Output** — JSON formatting with binary confidence scoring

The design philosophy is simple: **no answer is better than a wrong answer.**

## Key Features

- **Two research modes:** `precise_web_research()` for maximum accuracy, `web_research()` for faster single-step searches
- **Multi-provider support:** Anthropic, Google Gemini, Perplexity
- **Structured output:** Returns pandas DataFrames with answers and source URLs
- **Safety features:** Incremental CSV saving for long-running searches, automatic "Information unclear" responses when uncertain

## Installation and Usage

```bash
pip install llm-web-research
```

```python
import llm_web_research as lwr

results = lwr.precise_web_research(
    search_question="founding year",
    search_input=["Apple", "Microsoft"],
    api_key="your-api-key",
    model_source="anthropic"
)
```

## Use Cases

- Academic research requiring verified sources
- Fact-checking with high accuracy requirements
- Building high-quality datasets
- Automated due diligence tasks

Check out the [GitHub repository](https://github.com/chrissoria/llm-web-research) for full documentation and examples.

---

## Acknowledgments

This work was supported by the [Bashir Ahmed Graduate Fellowship](https://www.demog.berkeley.edu/about/ahmed-fellowship/) at UC Berkeley's Department of Demography. I am grateful to the Ahmed family and the Department of Demography for their support of my research.
