---
title: 'Ensemble Classification in CatLLM: Combining Multiple Models for Robust Results'
date: 2026-01-17
permalink: /posts/2026/01/catllm-ensemble-classification/
header:
  og_image: catllm_ensemble.png
tags:
  - CatLLM
  - Ensemble Methods
  - Large Language Models
  - Survey Data
  - Classification
---

![CatLLM](/images/catllm_ensemble.png)

<a href="https://pypi.org/project/cat-llm/">CatLLM</a> now supports ensemble classification—running multiple models in parallel and combining their predictions through voting. This addresses a persistent concern in LLM-based classification: how do you know if a single model's output is reliable?

## The Problem with Single-Model Classification

When you classify survey responses with a single LLM, you're trusting that model's interpretation entirely. But different models have different training data, different biases, and different failure modes. A response that GPT-4o categorizes as "positive sentiment" might be labeled "neutral" by Claude, and "mixed" by Gemini. Which one is right?

For research applications where classification decisions feed into statistical analyses, this uncertainty matters. Ensemble methods offer a way to quantify and reduce it.

## Three Approaches to Ensemble Classification

### 1. Cross-Provider Ensembles

You can combine models from different providers—OpenAI, Anthropic, Google, Mistral, and others—to get diverse perspectives on each classification:

```python
import catllm as cat

results = cat.classify(
    input_data=df['responses'],
    categories=["Positive", "Negative", "Neutral"],
    models=[
        ("gpt-4o", "openai", "sk-..."),
        ("claude-sonnet-4-5-20250929", "anthropic", "sk-ant-..."),
        ("gemini-2.5-flash", "google", "AIza..."),
    ],
    consensus_threshold="majority"
)
```

**Why this helps:** Each provider's models are trained on different data with different objectives. When three independently-developed models agree on a classification, that agreement carries more weight than any single model's confidence score. When they disagree, you've identified responses that may require human review.

### 2. Self-Consistency with Temperature

You can also ensemble the same model against itself by running it multiple times with higher temperature (randomness). This samples from the model's probability distribution rather than always taking the most likely output:

```python
results = cat.classify(
    input_data=df['responses'],
    categories=["Category A", "Category B", "Category C"],
    models=[
        ("gpt-4o", "openai", "sk-..."),
        ("gpt-4o", "openai", "sk-..."),
        ("gpt-4o", "openai", "sk-..."),
    ],
    creativity=0.7,  # Higher temperature for varied outputs
    consensus_threshold="majority"
)
```

**Why this helps:** At temperature 0, a model always produces the same output for the same input. At higher temperatures, it samples from its full distribution of possible responses. If a classification is robust, the model should arrive at the same answer even when sampling differently. If it produces different answers across runs, that response is likely ambiguous or borderline.

This approach is cheaper than cross-provider ensembles (one API key, often lower per-token costs) while still providing a measure of classification stability.

### 3. Consensus Thresholds

CatLLM provides three voting rules for determining consensus:

```python
# Majority: At least 50% of models must agree
consensus_threshold="majority"

# Two-thirds: At least 67% of models must agree
consensus_threshold="two-thirds"

# Unanimous: All models must agree
consensus_threshold="unanimous"
```

You can also specify custom numeric thresholds (e.g., `consensus_threshold=0.75` for 75% agreement).

**Majority** is the least restrictive. With three models, two agreeing is sufficient. This maximizes the number of responses that receive a consensus classification.

**Two-thirds** requires stronger agreement. With three models, you still need two to agree (67%), but with six models, you'd need four. This reduces false positives at the cost of more responses falling below threshold.

**Unanimous** is the most restrictive. Every model must agree for a category to be marked present. This produces high-confidence classifications but may leave many responses without consensus, flagging them for human review.

## Interpreting the Output

The results DataFrame includes columns for each model's individual classification plus the consensus:

| response | category_1_gpt_4o | category_1_claude | category_1_gemini | category_1_consensus |
|----------|-------------------|-------------------|-------------------|---------------------|
| "Great service" | 1 | 1 | 1 | 1 |
| "It was okay" | 0 | 1 | 0 | 0 |
| "Loved it" | 1 | 1 | 1 | 1 |

For the second response, GPT-4o and Gemini said "not positive" while Claude said "positive." With majority voting, the consensus is 0 (not positive) because only 1/3 models agreed.

You can use the agreement patterns to:
- Identify systematic differences between models
- Flag ambiguous responses for manual review
- Report inter-model reliability alongside your results

## Practical Considerations

**Cost:** Ensemble classification multiplies your API costs by the number of models. Three models means roughly 3x the cost. For large datasets, consider running ensembles on a sample first to calibrate, then using a single model for the full dataset.

**Speed:** Models are called in parallel, so wall-clock time doesn't increase linearly. Three models typically take only slightly longer than one.

**When to use ensembles:** Ensembles are most valuable when classification decisions are consequential—when they feed into regression models, when you're publishing findings, or when categories are subjective enough that reasonable people might disagree.

**When a single model suffices:** For exploratory analysis, prototyping, or cases where categories are unambiguous, a single model is faster and cheaper.

## Try It

Ensemble classification is available in CatLLM 0.1.16+ and in the [web app](https://huggingface.co/spaces/CatLLM/survey-classifier). In the web app, select "Model Comparison" to see each model's output side-by-side, or "Ensemble" to get majority-vote consensus classifications.

### Links

- **Web App:** [https://huggingface.co/spaces/CatLLM/survey-classifier](https://huggingface.co/spaces/CatLLM/survey-classifier)
- **Python Package:** [https://pypi.org/project/cat-llm/](https://pypi.org/project/cat-llm/)
- **GitHub:** [https://github.com/chrissoria/cat-llm](https://github.com/chrissoria/cat-llm)

If you have questions or want to discuss ensemble methods for your research, reach out at [ChrisSoria@Berkeley.edu](mailto:ChrisSoria@Berkeley.edu).
