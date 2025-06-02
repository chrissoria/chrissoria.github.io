---
title: "How We're Using OpenAI's GPT-4o for Dementia Classification"
date: 2025-06-02
permalink: /posts/2025/6/cat-llm-for-images/
tags:
  - Image Categorization
  - Vision Models
  - Large Language Models
  - Dementia
---

![CatLLM](/images/older_lady_drawing.png)

# Dementia Screening with AI: Analyzing Cognitive Drawing Tests

I work with the Caribbean American Dementia and Aging Study [(CADAS)](https://populationsciences.berkeley.edu/cadas/), where we're collecting nationally representative household survey data from adults aged 65+ in Puerto Rico and Dominican Republic, building upon the 10/66 Dementia Research Group's earlier work that revealed remarkably high dementia prevalence rates of 10-12% among older adults in these Caribbean communities.

We are building up towards various studies, all of which require an accurate classification of dementia (binary yes or no). One of the important elements that goes into this classification is whether the respondents from the study were able to draw a series of shapes well. However, we found some discrepancies in how the different interviewers were scoring the images (where interviewers seemed to be more and less harsh than each other). We decided that it would be great to have a second look at the images to better assess where things might be going wrong.

This challenge reflects broader problems in dementia diagnostics, where subjective human assessments often vary significantly between evaluators. After exploring various options, we decided to use OpenAI's GPT-4o model - a multimodal AI system with advanced vision capabilities - to analyze and classify these drawings. This approach aligns with [emerging research](https://www-nature-com.libproxy.berkeley.edu/articles/s41598-020-74710-9) showing that AI systems can provide [more consistent](https://www.nature.com/articles/s41591-024-03118-z) evaluation methods for cognitive assessments. Our experience highlighted the urgent need for standardized, objective assessment tools in dementia screening, which led us to develop the AI-based solution described in the following section.

## The Challenge of Manual Assessment

For decades, clinicians and researchers have relied on simple drawing tasks-like copying two overlapping pentagons-to help screen for dementia in older adults. Typically, these drawings are scored manually by trained professionals who assess whether the drawing meets specific criteria established by dementia researchers. The quality of these drawings, and particularly whether they accurately depict two intersecting pentagons, plays a significant role in determining cognitive status and potential dementia diagnosis.

However, this manual assessment process faces several critical challenges. As highlighted in research, traditional paper-based tests scored by humans often introduce inconsistencies and errors. When a single individual makes judgment calls on what constitutes correctly versus incorrectly drawn elements, scoring becomes subjective. Additionally, manually reviewing thousands of drawings is tedious, time-consuming, and costly. More traditionally trained deep learning models might also fail for this task given that the images often contain lots of non-relevant information-such as writing, instructions, and reference images-that aren't the drawings we're interested in. We need something that can truly **understand** where the actual drawing is on the image and distinguish it from other elements on the page.

## Our AI-Powered Approach

Our approach leverages AI models from OpenAI to transform this process. Using a tool called [CatLLM](https://pypi.org/project/cat-llm/), we combine vision models with language models (like GPT-4o) to automatically analyze these drawings and extract critical features. The AI evaluates specific elements-such as whether lines properly intersect or shapes are correctly closed-and assigns scores based on established criteria.

What makes this approach particularly valuable is our ability to compare AI assessments with human evaluations. Rather than having specialists review all 4,000 images in our dataset, they only need to examine the 400-800 cases where human and AI assessments differ-an efficiency improvement of 80-90%. This creates a powerful verification system where humans and AI complement each other's strengths.

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

## Privacy and Ethical Considerations

Importantly, our approach maintains strict privacy standards. While we work with thousands of drawings, none contain personally identifiable information. This ethical consideration is crucial, as researchers implementing similar systems should be mindful that sharing images with external AI providers could potentially expose sensitive information if proper precautions aren't taken.

## Conclusion

By leveraging AI in this manner, we're not just making the assessment process more efficient-we're potentially improving its accuracy and consistency, addressing a significant healthcare challenge in dementia screening.
