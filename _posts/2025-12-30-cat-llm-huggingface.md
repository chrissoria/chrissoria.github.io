---
title: 'CatLLM Now Supports Huggingface: Access Thousands of Open-Source Models'
date: 2025-12-30
permalink: /posts/2025/12/cat-llm-huggingface/
tags:
  - Huggingface
  - Open-Source Models
  - Large Language Models
  - Python Package
---

![CatLLM](/images/catllm_logo.png)

<a href="https://pypi.org/project/cat-llm/">**CatLLM**</a> now works with Huggingface! This is great news for researchers because it allows you to interact with open-weight and open-source models without needing to worry about having the compute power to run them locally. Just get your Huggingface API key (I recommend the Pro subscription for heavy usage—it's only $9/month) and you'll have access to models like Qwen, DeepSeek, and Llama. This is perfect for researchers who want to test open-weight models for their research or simply leverage their cheaper cost for classification tasks.

This is also great because it allows researchers to draw on thousands of user-trained models for specific tasks. For example:

- **MedAlpaca-7B (Medical Domain)** - `medalpaca/medalpaca-7b` - A 7-billion parameter LLM specifically fine-tuned for medical domain tasks, built on top of the LLaMA architecture. It's designed to improve question-answering and medical dialogue capabilities.

- **CodeLlama-7B (Code Generation & Understanding)** - `codellama/CodeLlama-7b-hf` - Meta's specialized code-focused LLM, available in 7B, 13B, 34B, and 70B parameter versions. It comes in three variants: base (general code), Python-specific, and Instruct (for code assistance).

- **Aya-23-8B (Multilingual)** - `CohereLabs/aya-23-8B` - Developed by Cohere Labs, Aya 23 is an instruction-tuned model with exceptional multilingual capabilities, supporting 23 languages including Arabic, Chinese, French, German, Hindi, Japanese, Korean, Spanish, and more.

Even more exciting is the possibility of training and hosting your own models. Hugging Face provides several tools for fine-tuning:

- **Transformers Library** - Use the Trainer API for fine-tuning any model from the Hub
- **PEFT (Parameter-Efficient Fine-Tuning)** - Techniques like LoRA and QLoRA for efficient fine-tuning with less compute
- **AutoTrain** - A no-code/low-code solution for fine-tuning models directly on Hugging Face
- **TRL (Transformer Reinforcement Learning)** - For RLHF and preference tuning

You can upload and host your models in several ways:

- **Web Interface** - Go to huggingface.co/new, then use "Add File" → "Upload File"
- **Python Libraries** - Use `model.push_to_hub("your-username/model-name")` with Transformers or the huggingface_hub library
- **Git** - Since repos are Git-based, you can push directly via command line

Your model doesn't need to be compatible with Transformers—any custom model works!

Imagine the possibilities for your research:

1. **Region-specific language models** - Fine-tune a model specifically for extracting information from Spanish-speaking respondents from a particular country, rather than Spanish generally. For example, a model trained on Dominican or Puerto Rican Spanish would better understand the distinct vocabulary, slang, and expressions that differ significantly from Mexican Spanish.

2. **Specialized scoring models** - Train a model specifically for detecting the quality of drawn shapes for cognitive impairment assessment. Instead of relying on general-purpose vision models, you could create one optimized for CERAD-style scoring tasks.

3. **Domain-specific extraction models** - Build a model designed to extract key details from long texts in your field—such as one trained to pull specific policy details from local city council meeting transcripts, or one that identifies funding amounts and grant recipients from foundation reports.

### Getting Started

Using Huggingface with CatLLM is straightforward. Simply specify `model_source="huggingface"` and provide your Huggingface API key:

```python
import catllm as cat

results = cat.multi_class(
    survey_input=df['responses'],
    categories=["Category 1", "Category 2", "Category 3"],
    api_key="your-huggingface-api-key",
    user_model="Qwen/Qwen3-VL-235B-A22B-Instruct:novita",
    model_source="huggingface",
    creativity=0,
    chain_of_thought=True
)
```

Here's an example using CodeLlama to analyze code snippets for specific features:

```python
import catllm as cat

# Analyze code snippets for security and quality features
code_analysis = cat.multi_class(
    survey_input=df['code_snippets'],
    categories=[
        "Contains SQL queries",
        "Has proper error handling",
        "Uses deprecated functions",
        "Contains hardcoded credentials",
        "Implements input validation"
    ],
    api_key="your-huggingface-api-key",
    user_model="codellama/CodeLlama-7b-Instruct-hf",
    model_source="huggingface",
    creativity=0,
    chain_of_thought=True
)
```

Here's an example using Aya-23 to classify Spanish survey responses with categories written in Spanish:

```python
import catllm as cat

# Classify Spanish survey responses about healthcare access
healthcare_analysis = cat.multi_class(
    survey_input=df['respuestas_encuesta'],
    categories=[
        "Este participante contestó que tiene acceso a seguro médico",
        "Este participante mencionó barreras financieras",
        "Este participante expresó dificultades con el idioma",
        "Este participante indicó satisfacción con su atención médica",
        "Este participante reportó largos tiempos de espera"
    ],
    api_key="your-huggingface-api-key",
    user_model="CohereLabs/aya-23-8B",
    model_source="huggingface",
    creativity=0,
    chain_of_thought=True
)
```

Here's an example using MedAlpaca to classify medical interview notes:

```python
import catllm as cat

# Classify patient interview notes for symptoms and conditions
medical_analysis = cat.multi_class(
    survey_input=df['patient_notes'],
    categories=[
        "Patient reports cardiovascular symptoms",
        "Patient mentions respiratory issues",
        "Patient describes chronic pain",
        "Patient indicates mental health concerns",
        "Patient reports medication side effects"
    ],
    api_key="your-huggingface-api-key",
    user_model="medalpaca/medalpaca-7b",
    model_source="huggingface",
    creativity=0,
    chain_of_thought=True
)
```

**Important Limitation:** MedAlpaca targets medical student-level knowledge and should never be used as a substitute for professional medical advice.

### Full Provider Support

CatLLM now supports seven major providers:

- OpenAI (GPT-4o, GPT-5)
- Anthropic (Claude Sonnet 4, Claude 3.5)
- Google (Gemini 2.5 Flash/Pro)
- **Huggingface** (Qwen, Llama, DeepSeek, community models)
- xAI (Grok)
- Mistral (Mistral Large, Pixtral)
- Perplexity (Sonar models)

### Get in Touch

If you have any questions about using Huggingface with CatLLM, or if you'd like guidance on how to fine-tune a model for your specific research needs to maximize consistency and quality of output, feel free to reach out. I'm happy to help researchers get the most out of these tools. You can contact me at [ChrisSoria@Berkeley.edu](mailto:ChrisSoria@Berkeley.edu).

### Learn More

- [View the documentation](https://github.com/chrissoria/cat-llm#readme)
- [Install from PyPI](https://pypi.org/project/cat-llm/): `pip install cat-llm`
