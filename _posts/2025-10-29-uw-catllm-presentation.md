---
title: 'Presenting CatLLM at the University of Washington'
date: 2025-10-29
permalink: /posts/2025/10/uw-catllm-presentation/
tags:
  - CatLLM
  - Large Language Models
  - Computational Social Science
  - Survey Research
  - Demography
---

On October 29th, 2025, I had the privilege of presenting at the University of Washington on how large language models can augment social science research. The presentation focused on [CatLLM](https://github.com/yourusername/catllm), an open-source Python package I developed to address a common challenge in demographic and social science research: analyzing open-ended survey responses and complex data at scale.

## The Challenge

During my PhD research on social networks and cognitive health in aging populations, I frequently encountered the time-consuming task of coding open-ended survey responses. Traditional approaches required either extensive manual coding or advanced machine learning expertise—neither of which was practical for many research workflows. This gap between the potential of modern AI tools and their accessibility to social scientists motivated me to create CatLLM.

## What is CatLLM?

CatLLM is a Python package that democratizes access to large language and vision models for research purposes. It enables researchers to:

- **Code open-ended survey responses** automatically and consistently
- **Analyze images** using vision models without computer vision expertise
- **Categorize and structure data** using natural language instructions
- **Apply state-of-the-art AI models** without needing machine learning backgrounds

The package is designed with social scientists in mind—prioritizing ease of use, reproducibility, and integration with existing research workflows.

## Near-Human Performance on Survey Categorization

The core focus of my presentation was demonstrating that large language models can achieve near-human performance on survey data categorization tasks. Using survey data categorization as a case study, I showed how LLMs can match the accuracy and consistency of trained human coders—a finding with significant implications for demographic and social science research.

However, a critical challenge when working with LLMs is their tendency to produce inconsistent or unstructured outputs. This is where CatLLM's key innovation comes in: **the package produces structured output categories 100% of the time**. This reliability transforms LLMs from an interesting but unpredictable tool into a dependable research instrument that researchers can confidently integrate into their workflows.

By guaranteeing structured outputs, CatLLM removes the technical barriers that often prevent researchers from leveraging LLMs in their work. Researchers no longer need to write complex parsing logic or handle edge cases—they can focus on their substantive research questions while CatLLM handles the technical complexity of working with language models.

## Open Science and Accessibility

CatLLM is fully open-source and available on [GitHub](https://github.com/yourusername/catllm) and [PyPI](https://pypi.org/project/catllm/). The package includes comprehensive documentation, tutorials, and examples to help researchers get started quickly. By making these tools accessible, I hope to enable more researchers to leverage the power of large language models in their work, regardless of their technical background.

## Looking Forward

The intersection of computational methods and demographic research continues to evolve rapidly. As large language models become more sophisticated, tools like CatLLM will play an increasingly important role in helping researchers analyze complex, unstructured data at scale. I'm excited to continue developing these tools and collaborating with researchers across disciplines to push the boundaries of what's possible in social science research.

---

*Chris Soria is a PhD candidate in Demography at UC Berkeley, where he studies how social networks shape cognitive health and dementia in aging populations. His work has been published in the American Journal of Epidemiology and The International Journal of Aging and Human Development, and presented at PAA, APHA, and PSA.*
