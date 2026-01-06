---
title: 'CatLLM is Now a Web App'
date: 2026-01-06
permalink: /posts/2026/01/catllm-web-app/
tags:
  - CatLLM
  - Web App
  - Large Language Models
  - Survey Data
  - Open Source
---

![CatLLM](/images/catllm_bw_banner.png)

I've been working on <a href="https://pypi.org/project/cat-llm/">CatLLM</a>, a Python package for classifying open-ended survey responses with LLMs. This week I converted it into a web app.

**Try it here:** [https://huggingface.co/spaces/chrissoria/CatLLM](https://huggingface.co/spaces/chrissoria/CatLLM)

## The Problem

If you've worked with open-ended survey data, you know the workflow: hundreds or thousands of free-text responses that need to be categorized before you can do any quantitative analysis. The traditional approach is manual coding—either doing it yourself or hiring RAs. It's slow, expensive, and doesn't scale.

## What the App Does

The web app lets you classify survey responses without writing any code:

1. **Upload your data** — CSV, Excel, or PDF documents
2. **Define categories** — Either specify your own categories or let the model extract them from your data automatically
3. **Run classification** — The model assigns each response to one or more categories (multi-label classification)
4. **Download results** — Get a CSV with classifications plus a methodology write-up you can adapt for your paper

The same functionality is available in the Python package if you prefer working in code, but the web app removes the setup barrier for researchers who just want to try it out.

## Free Models (For Now)

I'm covering the API costs temporarily so people can test it. The free tier currently includes:

- GPT-4o-mini (OpenAI)
- Claude 3 Haiku (Anthropic)
- Gemini 2.5 Flash (Google)
- Llama 3.3 70B (via Groq)
- DeepSeek V3.1
- Qwen3 235B
- Mistral Medium
- Grok 4 Fast

If you need more powerful models or have large-scale needs, you can bring your own API key.

## Looking for Feedback

This is still early. I'd appreciate it if you:

- **Break it** — Find edge cases, report bugs, tell me what fails
- **Suggest features** — What would make this useful for your research?
- **Collaborate** — If you're interested in working on a methods paper evaluating LLM classification for survey data, I'm open to it

You can reach me at [ChrisSoria@Berkeley.edu](mailto:ChrisSoria@Berkeley.edu) or leave comments on the [GitHub repo](https://github.com/chrissoria/cat-llm).

## Links

- **Web App:** [https://huggingface.co/spaces/chrissoria/CatLLM](https://huggingface.co/spaces/chrissoria/CatLLM)
- **Python Package:** [https://pypi.org/project/cat-llm/](https://pypi.org/project/cat-llm/)
- **GitHub:** [https://github.com/chrissoria/cat-llm](https://github.com/chrissoria/cat-llm)
