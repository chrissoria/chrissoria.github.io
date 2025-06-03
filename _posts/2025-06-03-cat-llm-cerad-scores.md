---
title: "Contribute to Open-Source Dementia Research: Improving CERAD Image Scoring"
date: 2025-06-03
permalink: /posts/2025/6/cat-llm-for-cerad-scores/
tags:
  - Image Categorization
  - Vision Models
  - Large Language Models
  - CERAD Score
---

We're developing an open-source tool to improve cognitive assessment and need collaborators for a research publication. We would benefit greatly from expert input by people who specialize in machine learning, deep learning, computer vision models, and related fields.

## What We're Building

We've created a function that automatically scores drawings from the CERAD Constructional Praxis test. This test asks patients to copy simple shapes like circles, diamonds, rectangles, and cubes. The quality of these drawings provides data points that feed into larger AI algorithms designed to classify dementia.

Our tool is a modified version of the CatLLM extract_image_multi_class function that has been adapted to output actual numerical scores based on CERAD scale criteria for each image, rather than simple categories.

## Current Functionality

The function can:
- Score drawings of different shapes using established Consortium to Establish a Registry for Alzheimer's Disease (CERAD) criteria
- Process individual images or batches of images
- Utilize different AI models (OpenAI, Anthropic, Perplexity, Mistral) for analysis
- Save progress to CSV files during processing
- Output structured scores that integrate with downstream dementia classification algorithms

```python
pip install cat-llm
import catllm as cat
circle_images_scored = cat.cerad_drawn_score(
    shape="circle",
    image_input=pr_cog['c_72_1_pic_path'].tolist(),
    api_key=open_ai_key,
    safety=True,
    reference_in_image=True,
    user_model="gpt-4o",
    filename=f"{save_path}/c_72_1_machine_score_full.csv",
)
```

## Areas for Improvement

We've identified several areas where contributions could enhance the tool's accuracy and utility:

**Model and Prompt Optimization**
- Refining prompts to improve scoring accuracy against CERAD criteria
- Testing alternative AI models better suited for medical image analysis
- Implementing model ensembling for more reliable scores
- Developing prompt ensembling techniques

**Image Processing**
- Preprocessing images to optimize them for AI analysis
- Expanding compatibility with tablet-drawn images
- Supporting various image formats and input methods

**Technical Enhancements**
- Improving computational efficiency and cost-effectiveness
- Enhancing error handling for edge cases
- Post-processing score calculations
- Expanding to other cognitive assessment tests like MMSE

## Research Publication Opportunity

This package will be submitted to academic journal and will be open-source and available to all. All contributors will be listed as co-authors on the publication, providing:

- Peer-reviewed publication credit
- Open-source software development experience
- Healthcare AI application portfolio building
- Collaboration in medical technology research

## How to Contribute

**Email**: Contact <a href="chrissoria@berkeley.edu">chrissoria@berkeley.edu</a> with questions or proposals

**Direct Development**: Make improvements directly to the <a href="https://github.com/chrissoria/cat-llm/blob/main/src/catllm/CERAD_functions.py">Git repository</a> and submit pull requests. We can provide test images for performance evaluation or run tests with your enhancements.

## Technical Skills Needed

We're seeking contributors with experience in:
- Machine learning model development and evaluation[1][3]
- Image processing and computer vision
- AI model comparison and optimization[1]
- Software efficiency and optimization
- Medical data processing
- Automated coding systems[2]

## Context and Impact

This tool addresses the need for standardized, reproducible scoring in cognitive assessment. Manual scoring introduces variability between assessors, while automated scoring provides consistent input data for dementia classification systems.

The function serves as one component in a larger pipeline where consistent image scoring enables more reliable downstream AI analysis for cognitive health assessment.

**Contact chrissoria@berkeley.edu or access our repository to begin contributing to this research effort.**