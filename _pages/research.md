---
permalink: /
title: "Research"
excerpt: "Research"
description: "Chris Soria's research on social networks, cognitive aging, dementia, and computational methods for social science. PhD Candidate in Demography at UC Berkeley."
author_profile: true
redirect_from:
  - /research/
  - /research.html
---

Chris Soria is a PhD candidate in Demography at the [University of California, Berkeley](https://www.demog.berkeley.edu/graduate-students/christopher-soria/), where he studies how social networks shape health and cognitive aging across diverse populations. His [NIH/NIA F31-funded](https://reporter.nih.gov/search/kHoWAniqj0iJsgXgWI3_mQ/project-details/11071776) dissertation examines how social network characteristics influence cognitive decline in older adults. He brings rigorous computational and AI methods to bear on substantive questions about networks, health, and aging. His work has been published in the *American Journal of Epidemiology*, *Neuroepidemiology*, and *BMC Geriatrics*, and presented at the Population Association of America (PAA), the American Public Health Association (APHA), and the American Association for Public Opinion Research (AAPOR).

Networks, Health & Aging
------
My primary research examines how social network structure and quality influence health and cognitive aging at both individual and population scales.

**Social isolation, loneliness, and cognitive decline.** Using longitudinal data from the Health and Retirement Study, I investigate how objective social isolation and subjective loneliness independently shape cognitive trajectories in older adults, with particular attention to post-COVID dynamics. This work forms the core of my dissertation, chaired by [William Dow](https://publichealth.berkeley.edu/people/william-dow), and is funded by an [NIH/NIA F31 fellowship](https://reporter.nih.gov/search/kHoWAniqj0iJsgXgWI3_mQ/project-details/11071776).

**New tie formation after network shocks.** In collaboration with [Claude Fischer](https://sociology.berkeley.edu/faculty/claude-s-fischer), I examine whether restoring lost connections or forming new ties after network disruptions can improve wellbeing and self-rated health, building on the concept of social network cognitive buffers.

**Social networks and mortality.** In collaboration with [Dennis Feehan](https://dennisfeehan.org/), I use measures from 21 billion Facebook friendships to examine how county-level network cohesiveness and diversity relate to U.S. mortality disparities. Network structure rivals traditional predictors like smoking and income in its association with mortality (revise and resubmit at *Demography*). [Preprint](https://osf.io/preprints/socarxiv/kvmx6_v3)

**Dementia classification across diverse settings.** I contribute to work assessing the [10/66 algorithm](https://academic.oup.com/aje/advance-article-abstract/doi/10.1093/aje/kwae470/7932838) for dementia classification, mapping methods validated in low- and middle-income countries to U.S. data—bridging my substantive interest in dementia with my methodological focus on algorithmic classification. Published in the *American Journal of Epidemiology*.

**Caribbean American Dementia and Aging Study (CADAS).** I am part of the [CADAS](https://bmcgeriatr.biomedcentral.com/articles/10.1186/s12877-025-06131-0) research team, a population-based study of aging and dementia in Cuba, the Dominican Republic, and Puerto Rico. Published in *BMC Geriatrics*.

Computational & AI Methods
------
I develop computational tools and methods that serve my substantive research on networks, health, and aging. Most of this work centers on [CatLLM](/catllm/) ([catllm.com](https://catllm.com)), an open-source Python and R toolkit I built for applying language and vision models to survey coding, image analysis, and data categorization. It emerged from challenges I encountered analyzing open-ended survey responses in my own research.

**The CatLLM toolkit.** A peer-reviewed software paper introduces CatLLM as a reproducible pipeline for LLM-powered text and image classification, with defaults calibrated against expert human coders across multiple survey datasets. Published in the *[Journal of Open Source Software](https://doi.org/10.21105/joss.09678)*.

**Benchmarking LLMs for survey coding.** [Scaling Open-Ended Survey Coding](https://osf.io/preprints/socarxiv/gjvcf_v1) validates CatLLM across 21 LLMs and finds that all models over-classify by default — precision lags 40–50 percentage points behind sensitivity — while ensembles of inexpensive open-weight models outperform the best individual cloud model (under review at the *Journal of Computational Social Science*).

**Model diversity over model size.** [Model Diversity Over Model Size](https://osf.io/preprints/socarxiv/er6mz_v1) shows that, across 16 LLMs and four open-ended survey questions, unanimous voting across diverse models corrects over-classification on subjectively ambiguous categories — with cross-provider diversity, not temperature or within-family size, as the active ingredient. As few as three diverse lower-tier models reliably exceed GPT-5 (revise and resubmit at *Public Opinion Quarterly*).

**Demographic patterns in LLM coding.** [High Agreement, Different Stories](https://osf.io/preprints/socarxiv/85kyd_v1) shows that leading LLMs reach 88–97% agreement with expert human coders across survey categorization tasks, while revealing that high per-category agreement can mask systematic differences in how models and humans handle ambiguity — and how thematic patterns diverge across demographic groups (revise and resubmit at *JSSAM*).

I am extending these methods to dementia research, developing algorithmic classification approaches that improve the consistency and scalability of dementia assessment across clinical settings — bridging my methodological and substantive research streams.

Partisanship & Health
------
**Partisan differences in health behaviors and respiratory disease dynamics.** With [Audrey Dorelien](https://soc.washington.edu/people/audrey-dorelien), [Ayesha Mahmud](https://vcresearch.berkeley.edu/faculty/ayesha-mahmud), and [Dennis Feehan](https://dennisfeehan.org/), I examine how partisan affiliation shapes health behaviors and contact patterns, and how these differences alter respiratory disease dynamics. Using data from the Berkeley Interpersonal Contacts Study, we show that Republicans report 20% more daily contacts, adopt protective behaviors at lower rates, and exhibit strong political homophily. Our simulations demonstrate that network structure can more than double the infection gap between partisan groups and shift epidemic peaks by up to 46 days. [Preprint](https://www.medrxiv.org/content/10.64898/2026.01.14.26344076v1)
