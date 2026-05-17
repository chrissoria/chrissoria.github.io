---
title: 'CatLLM is Now an R Package (Eight of Them, Actually)'
date: 2026-05-17
permalink: /posts/2026/05/cat-llm-r-packages/
header:
  og_image: catllm_bw_banner.png
tags:
  - CatLLM
  - R
  - Large Language Models
  - Survey Data
  - Open Source
---

![CatLLM](/images/catllm_bw_banner.png)

<a href="https://pypi.org/project/cat-llm/">CatLLM</a> started life as a Python package for classifying open-ended survey responses with LLMs. It still is — but a lot of the researchers I want to reach work in R, not Python. Asking a sociologist or demographer to spin up a Python project just to categorize a column of text responses is a friction tax most won't pay.

So I built the R layer. As of this week, **eight R packages** — `cat.stack`, `cat.survey`, `cat.vader`, `cat.ademic`, `cat.cog`, `cat.pol`, `cat.web`, and the `cat.llm` meta-package — are installable from [r-universe](https://chrissoria.r-universe.dev). They wrap the Python ecosystem via [reticulate](https://rstudio.github.io/reticulate/), expose the same `classify()`, `extract()`, `explore()`, and `summarize()` API, and return results bitwise-equivalent to the Python equivalents. There's no R-specific logic — it's a thin shim. But it means you can stay in your `tidyverse` pipeline.

## Why an R layer at all

A huge share of survey methodology, demography, sociology, political science, and public health work happens in R. The available options for those users have been (1) reticulate the Python package themselves, (2) round-trip data to a separate Python script, or (3) hand-code text by RA. The first is fiddly, the second is annoying, the third doesn't scale. A native R interface removes all three.

## Installation

```r
install.packages(
  "cat.llm",
  repos = c("https://chrissoria.r-universe.dev",
            "https://cloud.r-project.org")
)

library(cat.llm)
install_cat_stack()   # one-time Python backend setup
```

> **Not on CRAN yet.** Install from r-universe for now — the packages aren't on CRAN while the API stabilizes. R-universe is set up like an additional repo, so `install.packages()` works as usual.

> **Why the dot in `cat.llm`?** R's convention for multi-word package names uses a dot — like `data.table`, `R.utils`. The Python equivalents drop the dot (`catllm`, `catstack`, `catsurvey`, …). Use the dotted form in `library()` and `install.packages()`.

`install_cat_stack()` runs once. Under the hood it calls `pip install` for the Python backend packages and configures reticulate to find them. After that you don't think about Python again.

## A first classification — entirely local

The simplest way to verify the install is to classify a handful of responses with a local [Ollama](https://ollama.com) model. No API key, no cloud calls, no per-token cost.

In a terminal:

```bash
ollama pull qwen2.5:14b   # ~9 GB on disk, ~10 GB RAM to run
```

Then in R:

```r
library(cat.survey)

responses <- c(
  "The new wellness program is great, I've been using it daily.",
  "It's confusing and the app crashes constantly.",
  "I haven't tried it yet but it sounds promising."
)

# Verbose category descriptions classify several percentage points
# more accurately than short labels — especially for smaller local
# models like Qwen 14B below.
verbose_cats <- c(
  "Positive: The respondent expresses satisfaction, approval, or favorable sentiment.",
  "Negative: The respondent expresses dissatisfaction, frustration, or criticism.",
  "Neutral: The respondent is factual, ambivalent, or does not express clear sentiment.",
  "Other: The response does not fit any of the above categories."
)

results <- classify(
  input_data   = responses,
  categories   = verbose_cats,
  user_model   = "qwen2.5:14b",
  model_source = "ollama"
)

print(results)
```

You get back a data frame with one column per category and one row per response — a binary matrix ready to merge back into your main dataset. The Ollama server starts automatically the first time you call `classify()` with `model_source = "ollama"`; you don't have to manage `ollama serve` yourself.

To run the same example against a cloud model, swap `model_source = "ollama"` and `user_model = "qwen2.5:14b"` for `user_model = "gpt-5"` (or `"claude-sonnet-4-6"`, `"gemini-2.0-flash"`, etc.) and pass `api_key = Sys.getenv("OPENAI_API_KEY")`. Everything else stays the same.

## The eight packages

Each domain package depends on `cat.stack` (the shared classification engine) and adds parameters relevant to its data type.

| Package        | Domain                              | What it adds                                                |
|----------------|-------------------------------------|-------------------------------------------------------------|
| **cat.stack**  | General-purpose classification base | Core `classify()`, `extract()`, `explore()`, `summarize()`  |
| **cat.survey** | Open-ended survey responses         | `survey_question` parameter for question context            |
| **cat.vader**  | Social media posts                  | Threads/Bluesky metadata, sentiment-tuned defaults          |
| **cat.ademic** | Academic papers (OpenAlex)          | `journal_name`, `topic_name`, `paper_limit` fetchers        |
| **cat.cog**    | Cognitive assessment scoring        | `cerad_drawn_score()` for CERAD constructional praxis       |
| **cat.pol**    | Policy documents                    | Fetchers for city ordinances, federal laws, exec orders     |
| **cat.web**    | Web content (URL fetching)          | Auto-fetch URLs, inject domain + content-type metadata      |
| **cat.llm**    | Meta-package (installs all 7)       | Single install for the full ecosystem                       |

A few examples of what the domain-specific parameters look like:

**`cat.ademic`** — pull abstracts directly from OpenAlex and classify them by method:

```r
library(cat.ademic)

results <- classify(
  categories   = c("Quantitative", "Qualitative", "Mixed Methods"),
  journal_name = "American Sociological Review",
  paper_limit  = 100L,
  polite_email = "you@university.edu",
  api_key      = Sys.getenv("OPENAI_API_KEY")
)
```

No DataFrame to assemble — `journal_name` and `paper_limit` do the fetching for you.

**`cat.web`** — point at URLs and let the package render the page content before classification:

```r
library(cat.web)

results <- classify(
  input_data = c("https://example.com/post-1", "https://example.com/post-2"),
  categories = c("News", "Opinion", "Personal blog", "Documentation"),
  api_key    = Sys.getenv("OPENAI_API_KEY")
)
```

**`cat.cog`** — a single-purpose function for scoring CERAD constructional-praxis drawings (image input only, for clinical / cognitive-aging research):

```r
library(cat.cog)

score <- cerad_drawn_score(
  image_path = "path/to/participant-drawing.png",
  api_key    = Sys.getenv("OPENAI_API_KEY")
)
```

The remaining packages (`cat.survey`, `cat.vader`, `cat.pol`, `cat.stack`) all share the same `classify()` / `extract()` / `explore()` / `summarize()` API; the vignettes show domain-tuned examples for each.

## Verifying the install end-to-end

After cloning the parent repo, this one command installs all eight R packages from local source, sets up the Python backends, and runs a minimal classification per package:

```bash
OPENAI_API_KEY=sk-... Rscript r-package/test-all-packages.R
```

Expected output: `8 / 8 passed (0 failed, 0 skipped)`. CI runs the same script on every push.

## Caveats

- **Not on CRAN yet** — r-universe only while the API stabilizes.
- **Python ≥3.9 required.** `install_cat_stack()` runs `pip install` under the hood; if you don't have Python, reticulate will prompt you to install miniconda.
- **For Ollama workflows**, the Ollama binary is a separate download from [ollama.com](https://ollama.com/download). Local 7B–14B models trail frontier cloud models by a few percentage points on classification accuracy — fine for most survey work, worth validating against a labeled subsample for high-stakes coding.
- **`cat.cog` is single-function for now** — CERAD scoring on drawn-shape images. More cognitive instruments to come.

## Links

- **R packages docs:** [christophersoria.com/cat-llm/](https://christophersoria.com/cat-llm/)
- **Getting Started vignette:** [cat.llm/articles/getting-started](https://christophersoria.com/cat-llm/cat.llm/articles/getting-started.html)
- **Python Package:** [pypi.org/project/cat-llm/](https://pypi.org/project/cat-llm/)
- **GitHub:** [github.com/chrissoria/cat-llm](https://github.com/chrissoria/cat-llm)

If you run into trouble installing, hit a confusing error from reticulate, or want to suggest a domain wrapper that doesn't exist yet, reach out at [ChrisSoria@Berkeley.edu](mailto:ChrisSoria@Berkeley.edu).
