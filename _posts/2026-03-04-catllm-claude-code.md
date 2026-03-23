---
title: 'Classifying Open-Ended Survey Responses Directly in Claude Code'
date: 2026-03-04
permalink: /posts/2026/03/catllm-claude-code/
header:
  og_image: "catllm-claude-code-banner.png"
tags:
  - LLM
  - cat-llm
  - Claude Code
  - open source
  - NLP
  - survey research
---

![](/images/catllm-claude-code-banner.png)

My open-source package **[cat-llm](https://github.com/chrissoria/cat-llm)** has always been a Python-first tool: you install it, import it, write a script, run it. That works fine when you already have a pipeline set up. It's friction when you just want to quickly classify a CSV someone sent you and move on.

Claude Code — Anthropic's terminal-based coding agent — supports project-local slash commands: markdown files in `.claude/commands/` that inject a prompt and tool permissions when invoked. I added four of them to cat-llm. The result is that you can now classify survey data, extract categories, check your API keys, and run end-to-end tests without touching a Python file.

This post walks through the setup and shows what it looks like in practice using 40 rows of open-ended responses from the UCNets survey (variable `a19i`).

---

## Installation

```bash
pip install cat-llm
```

That's the only dependency. cat-llm pulls in pandas, tqdm, requests, openai, and anthropic automatically. For PDF classification support:

```bash
pip install cat-llm[pdf]
```

You'll also need at least one provider API key. cat-llm reads from environment variables automatically:

```bash
export OPENAI_API_KEY="sk-..."       # OpenAI / xAI
export ANTHROPIC_API_KEY="sk-ant-..."  # Anthropic
export GOOGLE_API_KEY="AIza..."      # Google
```

Or drop them in a `.env` file at your project root — cat-llm will pick them up.

---

## Adding the Claude Code Commands

Clone or navigate to your cat-llm working directory, then create the commands folder:

```bash
mkdir -p .claude/commands/catllm
```

Add four markdown files — `classify.md`, `extract.md`, `providers.md`, and `test.md` — each containing a prompt that describes what Claude should do when the command is invoked. The full command definitions are in the [cat-llm repository](https://github.com/chrissoria/cat-llm) under `.claude/commands/catllm/`.

Once the files exist, open (or reopen) a Claude Code session from the cat-llm project directory. Type `/catllm:` and tab-complete to see all four commands available.

---

## Checking Your Providers

Before classifying anything, run:

```
/catllm:providers
```

Claude detects which API keys are present in your environment, masks the values, and lists suggested model names for each configured provider:

```
=== cat-llm Provider Status ===

[OK] OpenAI / xAI
     Key: OPENAI_API_KEY = sk-p...k3Rw
     Models: gpt-5, gpt-4o-mini, grok-3

[OK] Anthropic
     Key: ANTHROPIC_API_KEY = sk-a...9xQz
     Models: claude-opus-4-6, claude-sonnet-4-6, claude-haiku-4-5-20251001

[ ] Google (GOOGLE_API_KEY not set)
[ ] Mistral (MISTRAL_API_KEY not set)
[ ] HuggingFace (HUGGINGFACE_API_TOKEN not set)

[OK] Ollama (local)
     llama3.2:latest
     mistral:latest

Configured: 2 provider(s)
```

---

## Classifying UCNets `a19i`

The UCNets survey includes an open-ended question (`a19i`) asking respondents about sources of social support. The raw responses are text — exactly what cat-llm is designed for.

I have 40 responses in a CSV. The first step is letting the data suggest its own categories rather than imposing a scheme from the outside. The `/catllm:extract` command runs cat-llm's `extract()` function, which samples random chunks of the responses, asks the model to name the recurring themes in each chunk, and returns a ranked frequency list:

```
/catllm:extract ucnets_a19i.csv --col response --model gpt-5
```

```
=== Extracting categories from ucnets_a19i.csv ===
Column: response | Rows: 40 | Model: gpt-5

Discovered categories (ranked by frequency):
  1. Family and close relationships       (found in 18/20 chunks)
  2. Friends and peer support             (found in 15/20 chunks)
  3. Professional or institutional help   (found in 12/20 chunks)
  4. Online communities                   (found in 9/20 chunks)
  5. Religious or spiritual community     (found in 8/20 chunks)
  6. No support or social isolation       (found in 7/20 chunks)
  7. Coworkers or colleagues              (found in 5/20 chunks)

Suggested follow-up:
  /catllm:classify ucnets_a19i.csv \
    --col response \
    --categories "Family and close relationships,Friends and peer support,Professional or institutional help,Online communities,Religious or spiritual community,No support or social isolation,Coworkers or colleagues" \
    --output ucnets_a19i_classified.csv
```

The command even generates the follow-up classify call. Running it:

```
/catllm:classify ucnets_a19i.csv \
  --col response \
  --categories "Family and close relationships,Friends and peer support,Professional or institutional help,Online communities,Religious or spiritual community,No support or social isolation,Coworkers or colleagues" \
  --model gpt-5 \
  --output ucnets_a19i_classified.csv
```

```
=== Classifying ucnets_a19i.csv ===
Column: response | Rows: 40 | Model: gpt-5
Categories: 7

   response                                          family  friends  professional  online  religious  isolated  coworkers
0  My sister and I talk every day, she really...        1       0          0          0         0          0         0
1  Mostly just online — Reddit communities wh...        0       0          0          1         0          0         0
2  My church group has been incredible, they ...        0       1          0          0         1          0         0
3  Honestly nobody. I've felt very alone thr...         0       0          0          0         0          1         0
4  My therapist and my wife, in that order...          1       0          1          0         0          0         0
...

--- Category Distribution (40 rows) ---
Family and close relationships      29  (72.5%)
Friends and peer support            18  (45.0%)
Professional or institutional help  11  (27.5%)
Religious or spiritual community     9  (22.5%)
Online communities                   8  (20.0%)
No support or social isolation       6  (15.0%)
Coworkers or colleagues              4  (10.0%)

Saved to ucnets_a19i_classified.csv
```

The output is a binary matrix — one column per category, one row per response. A single response can belong to multiple categories simultaneously, which is the right design for this kind of data: someone who mentions both their sister and their therapist gets a 1 in both `family` and `professional`, not a forced choice between them.

The classified CSV is ready for any downstream analysis — R, Stata, Python, whatever the pipeline requires.

---

## Running the Quick Test

There's also a built-in smoke test command that runs on the package's bundled example data:

```
/catllm:test
```

```
=== cat-llm Quick Test ===
File: examples/test_data/survey_responses.csv
Model: gpt-5
Categories: ['Positive', 'Negative', 'Neutral']

Loaded 20 rows. Columns: ['id', 'response']
Text column: response

--- Results ---
    response                                          Positive  Negative  Neutral
0   The program was incredibly helpful and I...           1        0        0
1   I didn't find the sessions useful at all...           0        1        0
2   It was okay, nothing special but not bad...           0        0        1
...

--- Category Distribution ---
Positive    11
Negative     5
Neutral      4

PASS: classify() completed successfully.
```

Useful for verifying a new API key or model name works before pointing it at real data.

---

## What Else You Can Do

The commands are thin wrappers around cat-llm's Python API, which has considerably more surface area:

**Multi-model ensemble.** Pass a list of models and cat-llm runs all of them in parallel, then reports a consensus column alongside each model's individual output. Disagreements across models are flagged automatically.

```python
import catllm as cat

result = cat.classify(
    input_data,
    categories,
    models=[
        ("gpt-5",                "openai",    openai_key,    {}),
        ("claude-sonnet-4-6",    "anthropic", anthropic_key, {}),
        ("gemini-2.0-flash",     "google",    google_key,    {}),
    ],
    consensus_threshold="unanimous",
)
```

**Extended reasoning.** Pass `thinking_budget=4096` (Anthropic) or `chain_of_thought=True` for borderline classification tasks where you want the model to reason before committing to a label.

**PDF classification.** If `input_data` points at a directory of PDFs, cat-llm renders each page and classifies the content as images. Useful for document archives or grant applications.

**Category discovery.** `cat.extract()` is the same function the `/catllm:extract` command calls under the hood. You can run it directly, tune the `iterations` and `divisions` parameters, and use the raw frequency table to build a codebook before any classification happens.

---

The cat-llm repository is at **[github.com/chrissoria/cat-llm](https://github.com/chrissoria/cat-llm)** and the package is on PyPI as `cat-llm` (version 2.5.1 as of this writing). If you adapt the Claude Code commands for a different workflow or build something interesting with the package, reach out at [chrissoria@berkeley.edu](mailto:chrissoria@berkeley.edu).
