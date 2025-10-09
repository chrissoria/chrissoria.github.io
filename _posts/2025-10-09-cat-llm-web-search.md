---
title: 'CatLLM Now Builds Custom Datasets from Web Data'
date: 2025-10-09
permalink: /posts/2025/10/cat-llm-web-research/
tags:
  - Web Research
  - Dataset Construction
  - Large Language Models
  - Python Package
---

![CatLLM](/images/web_search_cat_llm.png)

We've added a powerful new feature to <a href="https://pypi.org/project/cat-llm/">**CatLLM**</a> that helps researchers construct custom datasets from scratch using unstructured web data.

Social scientists often need to gather information about people, organizations, or events that isn't available in a single database. Previously, this meant hours of manual web searches and data entry. Now, CatLLM can automatically search the web and extract structured information, turning endless online data into research-ready datasets.

### How It Works

The `build_web_research_dataset` function takes a list of search subjects (names, companies, locations, etc.) and a research question, then searches the web to compile your answers into a structured dataset. The function currently works with Anthropic and Google models, with Perplexity search implementation on the horizon.

Here's a simple example that gathers academic department information for UC Berkeley faculty:

```
import catllm as cat

list_names = ["Chris Soria", "Matthew Stenberg", "Sara Quigley"]

test = cat.build_web_research_dataset(
search_question="Academic Department they belong to at UC Berkeley?",
search_input=list_names,
api_key=api_key,
answer_format="just the department name",
time_delay=5, # I recommend a time delay of at least 5 seconds to avoid rate limiting
user_model="claude-sonnet-4-20250514")
```

### Example Use Cases

The function works for a wide range of research questions:

- **Climate research**: What is the hottest temperature on record for these cities?
- **Policy analysis**: What kind of COVID restrictions did this county have in 2021?
- **Political science**: What political party did this county's mayor belong to in 2024?
- **Career outcomes**: Where did this person end up after they got their PhD from Berkeley in 2023?

### Beta Testing

Results are currently being beta tested—thank you to UC Berkeley Graduate Division for helping us refine this feature. Early results show that the function can save researchers dozens of hours on data collection tasks while maintaining high accuracy for factual information.

Whether you're building a dataset of company headquarters, tracking organizational affiliations, or gathering biographical information for your study, this new feature transforms web research from a manual slog into an automated workflow.

### Learn More

- [View examples on GitHub](https://github.com/chrissoria/cat-llm/blob/main/examples/Building%20a%20Dataset%20From%20the%20Web.ipynb)
- [Install from PyPI](https://pypi.org/project/cat-llm/)
- [Read the research paper](https://github.com/chrissoria/cat-llm/blob/main/academic_examples/paper.pdf)