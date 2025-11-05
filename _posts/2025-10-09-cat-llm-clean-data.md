---
title: 'Cleaning data with AI: An example with CatLLM'
date: 2025-11-05
permalink: /posts/2025/10/cat-llm-clean-data/
tags:
  - Data Science
  - Cleaning data
  - Large Language Models
  - Python
---

# Using CatLLM to Flag Sensitive Information in Survey Data

Data cleaning is one of the most time-consuming tasks in data science, especially when dealing with open-ended survey responses that may contain personally identifiable information (PII). Traditional approaches require manual review or complex regex patterns, but Large Language Models offer a more intelligent solution. CatLLM provides a streamlined way to automatically classify text data based on custom categories, making it particularly useful for identifying sensitive information in research datasets.

## The Challenge of PII Detection

When collecting qualitative survey data, respondents sometimes include specific details like their names, exact addresses, or other identifying information. Before sharing or publishing this data, researchers need to identify and redact these responses. Manually reviewing thousands of responses is impractical, and rule-based approaches often miss context-dependent cases. This is where LLM-based classification shines—models can understand nuance and context in ways that simple pattern matching cannot.

## An Important Privacy Consideration

**Before implementing any LLM-based approach for sensitive data, it's crucial to use model providers that guarantee data privacy.** For example, UC Berkeley uses Google's Gemini models specifically because Google promises not to use institutional data for training purposes and maintains strict privacy and security protocols. Similarly, other institutions might use Azure OpenAI with enterprise agreements, or on-premises models. Never send sensitive data to public APIs or services that don't have explicit data privacy guarantees.

## How CatLLM Simplifies Classification

CatLLM allows you to define custom categories and automatically classify text responses. In the example below, we're processing multiple survey datasets to flag responses that contain specific identifying information. The library handles the complexity of prompt engineering, API calls, and result aggregation, letting you focus on defining meaningful categories.

## Code Example

```
import pandas as pd
import catllm as cat

# Load survey responses
df = pd.read_csv('survey_responses.csv')

# Define classification categories
categories = [
    'contains identifiable information (name, address)', 
    'does not contain sensitive information'
]

# Classify each response for PII
results = cat.multi_class(
    survey_input=df['Response'],
    user_model='gemini-1.5-pro',  # Using privacy-compliant model
    categories=categories,
    filename='flagged_responses.csv',
    api_key=api_key
)

print(f"✓ Classified {len(df)} responses")
```

To use this code, you'll first need to install the CatLLM library (pip install cat-llm) and obtain an API key from your chosen LLM provider (in this example, we use Google's Gemini, which requires a Google Cloud API key with appropriate privacy guarantees). When you run the code, CatLLM will send each response to the language model along with your category definitions, and the model will determine which category best fits each response. The results are saved to flagged_responses.csv, which includes the original responses along with their assigned classifications. This allows you to quickly identify which responses contain personally identifiable information that may need redaction before sharing your data. 

## Benefits and Applications

This approach scales effortlessly—whether you have hundreds or millions of responses, the classification process remains consistent. Beyond PII detection, you can use this same framework to categorize responses by sentiment, topic, urgency, or any other dimension relevant to your research. The results are saved as CSV files, making it easy to integrate with existing data pipelines and conduct follow-up analyses.

## Best Practices

When implementing LLM-based data cleaning, always validate results on a sample before processing your entire dataset. Consider having human reviewers check a random subset of classifications to ensure accuracy. Document which model and categories you used for reproducibility, and maintain clear audit trails of any data transformations. Most importantly, ensure your approach complies with your institution's IRB protocols and data governance policies, especially when handling sensitive information.

### Learn More

- [View examples on GitHub](https://github.com/chrissoria/cat-llm/blob/main/examples/Building%20a%20Dataset%20From%20the%20Web.ipynb)
- [Install from PyPI](https://pypi.org/project/cat-llm/)
- [Read the research paper](https://github.com/chrissoria/cat-llm/blob/main/academic_examples/paper.pdf)