---
layout: archive
title: "CenSoc Project"
permalink: /censoc/
author_profile: true
---

## About the CenSoc Project

<a href="https://censoc.berkeley.edu/about-the-censoc-project/" target="_blank">The CenSoc project</a> – so named because it links 1940 Census data with Social Security Administration death records – is a new, large-scale, public microdata data set to be used for advancing understanding of mortality disparities in the United States.

The project uses record linkage techniques to match deaths aged 65-and-over observed from 1975 to 2005 back to individual, family, and neighborhood characteristics in the census. The use of modern data-linkage techniques allows us to construct datasets of about 4.7-7 million records, several times the size of the largest existing sample surveys.

We also publish the Berkeley Unified Numident Mortality Database (BUNMD), a standalone file containing over 49 million death records, and World War II era Army enlistment records.

The unprecedented scale and detail of CenSoc data allow researchers to make new discoveries in areas such as:
- Mortality disparities by education, national origin, and race
- Early life conditions and later-life mortality
- Geographic variation and the neighborhood determinants of mortality

These topics are of increasing importance in understanding increases in disparities in life expectancy in the United States.

## My Contribution

The <a href="https://github.com/caseybreen/censocdev/tree/master/codebase/09_geography_files" target="_blank">code in this directory</a> generates the BUNMD and CenSoc-Numident supplemental geography files. We use raw data on ZIP code at death and city of birth to infer birth city, death state, death county, and more.

- The BUNMD supplemental geography file can be merged to the BUNMD using SSN.
- The CenSoc-Numident supplemental geography file can be merged onto the CenSoc-Numident with HISTID.

**Compatibility (August 2023):**
- The BUNMD supplemental geography is compatible with BUNMD 2.0.
- The CenSoc-Numident supplemental geography file is compatible with CenSoc-Numident 2.1 (conservative links only) and CenSoc 3.0.
