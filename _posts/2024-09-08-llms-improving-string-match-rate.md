---
title: 'How to Improve Match Quality on String Data Using Large Language Models'
date: 2024-09-08
permalink: /posts/2024/09/llm-string-match1/
tags:
  - LLM
  - string data
  - data cleaning
---

In the world of data analysis, ensuring the accuracy and consistency of datasets is crucial, especially when dealing with entities like school names that may be spelled differently across various sources. This discrepancy can pose significant challenges when trying to match records from different datasets. Traditional methods of data cleaning may fall short in addressing these inconsistencies effectively.

In this blog post, we explore an innovative approach to improving match quality between datasets using Large Language Models (LLMs) and the Jaro-Winkler similarity algorithm. By leveraging the power of LLMs, we can "force" both datasets to align more closely in their naming conventions, enhancing the probability of finding accurate matches. The Jaro-Winkler score then helps us identify the highest probability matches, ensuring that our data integration efforts are both efficient and reliable.

Follow along below or download the python script here: https://github.com/chrissoria/chrissoria.github.io/blob/main/files/clean_schools.ipynb

## Overall Summary of the Post

- **I take two datasets and push the match rate from 23.83% to 67.16% using generative AI.**
- **this post was written by GPT4**

### Getting set up

Before diving into the data processing, it's essential to set up the environment with the necessary libraries and configurations. Here's a breakdown of the initial steps:


```python
from openai import OpenAI
import pandas as pd
import jellyfish
import numpy as np
import json
import os
import re
import time
from dotenv import load_dotenv, find_dotenv
```

To keep sensitive information like API keys secure, we use environment variables. The dotenv library helps us load these variables from a local .env file:

```python
load_dotenv()
```




    True


This command initializes the environment variables, making them accessible within the script. It ensures that API keys and other sensitive data are not hard-coded into the script. The script also specifies different models (gpt-3.5-turbo-16k, gpt-3.5-turbo, gpt-4o) for potential use, each offering different capabilities and token limits.

```python
_ = load_dotenv(find_dotenv()) # read local .env file

#openai.api_key = os.getenv("api.txt")
LONG_MODEL = "gpt-3.5-turbo-16k"
GPT_3 = "gpt-3.5-turbo"
GPT_4 = "gpt-4o"
```

To ensure that the script operates in the correct context, we set the working directory to the location of our datasets:

```python
os.chdir('/Users/chrissoria/Documents/Research/determinants-grad-adm')
current_directory = os.getcwd()
print(current_directory)
```

    /Users/chrissoria/Documents/Research/determinants-grad-adm


### Cleaning School Names

To begin, we define a function to clean the school names by standardizing their format. This involves converting text to lowercase, removing unwanted characters, and trimming whitespace. This function does the following:
- **Lowercasing**: Converts all text to lowercase to ensure case-insensitive comparisons.
- **Removing Punctuation**: Eliminates commas and hyphens to reduce variability in naming.
- **Trimming Whitespace**: Strips leading and trailing spaces and replaces multiple spaces with a single space.
- **Removing Articles**: Removes the word "the" from the start of names to focus on the core name.

Here's the function:

```python
def clean_school_names(df, column_name):
    df[column_name] = df[column_name].str.lower()
    df[column_name] = df[column_name].str.replace(r'[,-]', '', regex=True)
    df[column_name] = df[column_name].str.strip()
    df[column_name] = df[column_name].str.replace(r'\s+', ' ', regex=True)
    df[column_name] = df[column_name].str.replace(r'^the\s+', '', case=False, regex=True)
    return df
```

Next, we load the Berkeley schools dataset, select the relevant column, and apply our cleaning function.

- **Loading Data**: Reads the Excel file containing school names.
- **Selecting Columns**: Focuses on the column with undergraduate degree school names.
- **Renaming Columns**: Renames the column for consistency in further processing.

After cleaning, we ensure that each school name is unique:

```python
berkeley_schools = pd.read_excel('data/berkeley_schools.xlsx')
berkeley_schools = berkeley_schools[['UG Degree School']]
berkeley_schools = berkeley_schools.rename(columns = {'UG Degree School' : 'school'})
print(len(berkeley_schools))
berkeley_schools.head()
```

    158007





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>University of Kentucky</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Technion-Israel Inst of Tech</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Minnesota, Twin Cities</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Univ of Nairobi</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Southern California</td>
    </tr>
  </tbody>
</table>
</div>


Similarly, we load and prepare the IPEDS schools dataset:

```python
berkeley_schools = clean_school_names(berkeley_schools, 'school')

berkeley_schools = pd.DataFrame(berkeley_schools['school'].dropna().unique(), columns=['school'])

print(len(berkeley_schools))
berkeley_schools.head()
```

    5166





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
    </tr>
    <tr>
      <th>1</th>
      <td>technionisrael inst of tech</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of minnesota twin cities</td>
    </tr>
    <tr>
      <th>3</th>
      <td>univ of nairobi</td>
    </tr>
    <tr>
      <th>4</th>
      <td>university of southern california</td>
    </tr>
  </tbody>
</table>
</div>


## Preparing and Matching the IPEDS Schools Dataset

Continuing with our data preparation, we now focus on the IPEDS schools dataset. This dataset contains a comprehensive list of institutions, which we will clean and prepare for matching with the Berkeley schools dataset.

First, we load the dataset and select the relevant column containing school names:

```python
iped_schools = pd.read_csv('data/IPEDS_schools.csv')
iped_schools = iped_schools[['INSTNM']]
iped_schools = iped_schools.rename(columns = {'INSTNM' : 'school'})
print(len(iped_schools))
iped_schools.head()
```

    /var/folders/89/6bdxzk2j30v5n3wstywbcpg80000gn/T/ipykernel_17234/287998861.py:1: DtypeWarning: Columns (9,1537,1540,1542,1606,1608,1614,1615,1619,1620,1621,1622,1623,1624,1625,1626,1627,1628,1629,1703,1704,1725,1726,1727,1728,1729,1743,1815,1816,1817,1818,1823,1824,1830,1831,1879,1880,1881,1882,1883,1884,1885,1886,1887,1888,1889,1890,1891,1892,1893,1894,1895,1896,1897,1898,1909,1910,1911,1912,1913,1957,1958,1959,1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1983,1984,2376,2377,2403,2404,2495,2496,2497,2498,2499,2500,2501,2502,2503,2504,2505,2506,2507,2508,2509,2510,2511,2512,2513,2514,2515,2516,2517,2518,2519,2520,2521,2522,2523,2524,2525,2526,2527,2528,2529,2530,2958) have mixed types. Specify dtype option on import or set low_memory=False.
      iped_schools = pd.read_csv('data/IPEDS_schools.csv')


    6543





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Alabama A &amp; M University</td>
    </tr>
    <tr>
      <th>1</th>
      <td>University of Alabama at Birmingham</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Amridge University</td>
    </tr>
    <tr>
      <th>3</th>
      <td>University of Alabama in Huntsville</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Alabama State University</td>
    </tr>
  </tbody>
</table>
</div>

We apply the same cleaning function to standardize the school names in the IPEDS dataset:


```python
iped_schools = clean_school_names(iped_schools, 'school')

iped_schools = pd.DataFrame(iped_schools['school'].dropna().unique(), columns=['school'])

#for assesing a match rate I'll add a 1 to the df
iped_schools['match'] = 1

print(len(iped_schools))
iped_schools.head()
```

    6405





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>match</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alabama a &amp; m university</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>university of alabama at birmingham</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>amridge university</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>university of alabama in huntsville</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>alabama state university</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



With both datasets cleaned and prepared, we can now attempt to match them based on the school names. There are 5,222 unique schools in the Berkeley list and 6,543 in the IPEDS data. Our goal is to maximize the match rate, with the highest possible match being 5,222.


```python
highest_possible_match = len(berkeley_schools)
```

We perform a left join to match the datasets based on the school column:


```python
merged_1 = berkeley_schools.merge(iped_schools, on= 'school', how = 'left')
merged_1.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>match</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>technionisrael inst of tech</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of minnesota twin cities</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>univ of nairobi</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>university of southern california</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
print(f"The match rate with standardizing strings in both columns and nothing more is {merged_1['match'].sum() / highest_possible_match * 100:.2f}%")
```

After standardizing the school names in both datasets, we achieved a match rate of 23.83%. While this is a good start, we can further improve the match rate by employing fuzzy matching techniques. Fuzzy matching helps us account for minor differences in spelling and avoid false matches between schools with similar names.

### Applying the Jaro-Winkler Algorithm

To enhance our matching process, we utilize the Jaro-Winkler similarity algorithm. This algorithm is particularly effective for comparing strings and identifying matches based on a similarity score. Here's how we implement it:


```python
def find_best_match(school, choices, threshold=0.975):
    best_match = None
    highest_score = 0
    for choice in choices:
        score = jellyfish.jaro_winkler(school, choice)
        if score > highest_score:
            best_match = choice
            highest_score = score
    if highest_score >= threshold:
        return best_match, highest_score
    else:
        return None, highest_score

# Apply the matching function to each school name in berkeley_schools
matches = berkeley_schools['school'].apply(lambda x: find_best_match(x, iped_schools['school']))

# Create new columns for the best match and match score
berkeley_schools['Best Match'] = matches.apply(lambda x: x[0])
berkeley_schools['Match Score'] = matches.apply(lambda x: x[1])

berkeley_schools.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>Best Match</th>
      <th>Match Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>technionisrael inst of tech</td>
      <td>None</td>
      <td>0.828889</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
    </tr>
    <tr>
      <th>3</th>
      <td>univ of nairobi</td>
      <td>None</td>
      <td>0.857179</td>
    </tr>
    <tr>
      <th>4</th>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>


- **Function Definition**: The find_best_match function iterates through possible matches and calculates the Jaro-Winkler score for each.
- **Threshold Setting**: We set a high threshold (0.975) to ensure that only highly similar matches are considered valid.
- **Applying the Function**: We apply the function to each school name in the Berkeley dataset to find the best match in the IPEDS dataset.

The results of the fuzzy matching process are promising. Here's a sample of the output:

```python
filtered_matches = berkeley_schools[berkeley_schools['Match Score'] >= 0.975]

merged_2 = filtered_matches.merge(iped_schools, left_on='Best Match', right_on='school', suffixes=('_left', '_right'), how='left')
merged_2.head()
```

**Perfect Matches**: Some schools, like "University of Kentucky" and "University of Southern California," achieve a perfect match score of 1.0.
**Partial Matches**: For schools with lower scores, such as "Technion-Israel Inst of Tech," the algorithm did not find a sufficiently similar match.


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school_left</th>
      <th>Best Match</th>
      <th>Match Score</th>
      <th>school_right</th>
      <th>match</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
      <td>university of kentucky</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
      <td>university of minnesotatwin cities</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
      <td>university of southern california</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>brown university</td>
      <td>brown university</td>
      <td>1.000000</td>
      <td>brown university</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>colorado school of mines</td>
      <td>colorado school of mines</td>
      <td>1.000000</td>
      <td>colorado school of mines</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



```python
print(f"The match rate with standardizing strings and a jaro-winkler threshold of .975 is {merged_2['match'].sum() / highest_possible_match * 100:.2f}%")
```

    The match rate with standardizing strings and a jaro-winkler threshold of .975 is 26.93%


## Enhancing Data Matching with AI Assistance

While our initial fuzzy matching using the Jaro-Winkler algorithm improved the match rate to 26.93%, we encountered a challenge: some entries in the Berkeley list are either international schools or not schools at all. To address this, we leverage the power of GPT to identify and filter valid domestic schools.

We use GPT to determine which entries in the Berkeley dataset are valid schools and whether they are located in the United States. This step helps us focus our matching efforts on relevant entries, potentially improving the match rate.


```python
def identify_valid_schools(school_list,
                     user_model):
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    standardized_schools = []
    
    example_json = """{"country": "United States"}"""
    
    for school in school_list:
        prompt = f"""Tell me which country the college in triple backtics is located in: ```{school}```. \
        Put your response in JSON format with 'country' as the key and your output as the value. \
        If it's not a valid school make the value be 'invalid'. \
        Here's an example of what the JSON should look like: {example_json}"""
        try:
            response = client.chat.completions.create(
                model=user_model,
                response_format={"type": "json_object"},
                messages=[
                    {
                      "role": "system",
                      "content": f"""You provide direct and concise responses and provide only the answer to the question asked and provide only the requested JSON and nothing more."""
                    },
                    {'role': 'user', 
                     'content': prompt}
                ],
                temperature=0
            )


            standardized_school = response.choices[0].message.content
            standardized_schools.append(standardized_school)
            print(f"Processing row {school}")
        except Exception as e:
            print(f"An error occurred: {e}")
            standardized_schools.append(f"Error processing input: {school}")
            print('error tho')
            
    data = []
    
    for item in standardized_schools:
        parsed_json = json.loads(item)
        data.append(parsed_json)
        
    df = pd.DataFrame(data)
    standardized_schools = df['country']
    
    return standardized_schools
```
- **Functionality**: This function queries GPT to identify the country of each school or mark it as invalid if it's not a recognized institution.
- **JSON Response**: The response is formatted as JSON, making it easy to parse and use in further analysis.

We apply the identify_valid_schools function to the Berkeley dataset and create a new column to indicate whether each school is domestic:

```python
berkeley_schools['country'] = identify_valid_schools(berkeley_schools['school'],
                                                          GPT_4)

```
To improve the accuracy of our data matching, we added a domestic indicator to the Berkeley schools dataset. This step helps us focus on schools located in the United States, which are more relevant for our matching purposes.

We created a new column, `domestic`, to indicate whether each school is located in the United States. This column is populated based on the `country` information obtained from GPT:

```python
berkeley_schools['domestic'] = berkeley_schools['country'].apply(lambda x: 1 if 'United States' in x else 0)
berkeley_schools.to_csv('data/berkeley_schools_features.csv')
berkeley_schools
```

Domestic Indicator: The domestic column is set to 1 for schools in the United States and 0 for others.
Data Export: The updated dataset is saved for future reference and analysis.


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>Best Match</th>
      <th>Match Score</th>
      <th>country</th>
      <th>domestic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>technionisrael inst of tech</td>
      <td>None</td>
      <td>0.828889</td>
      <td>Israel</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>univ of nairobi</td>
      <td>None</td>
      <td>0.857179</td>
      <td>Kenya</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5161</th>
      <td>pec university of technology (deemed to be uni...</td>
      <td>None</td>
      <td>0.736349</td>
      <td>India</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5162</th>
      <td>louisiana college</td>
      <td>None</td>
      <td>0.878834</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5163</th>
      <td>niger</td>
      <td>None</td>
      <td>0.711111</td>
      <td>invalid</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5164</th>
      <td>university of nebraska omaha</td>
      <td>None</td>
      <td>0.966359</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5165</th>
      <td>centro universitario catolico salesiano auxilium</td>
      <td>None</td>
      <td>0.841793</td>
      <td>Brazil</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5166 rows × 5 columns</p>
</div>


## Filtering and Merging for Improved Matches
With the domestic indicator in place, we filter the dataset to focus on high-confidence matches and merge it with the IPEDS dataset:

```python
filtered_matches_domestic = berkeley_schools[berkeley_schools['Match Score'] >= 0.975]

merged_2 = filtered_matches.merge(iped_schools, left_on='Best Match', right_on='school', suffixes=('_left', '_right'), how='left')
merged_2.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school_left</th>
      <th>Best Match</th>
      <th>Match Score</th>
      <th>school_right</th>
      <th>match</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
      <td>university of kentucky</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
      <td>university of minnesotatwin cities</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
      <td>university of southern california</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>brown university</td>
      <td>brown university</td>
      <td>1.000000</td>
      <td>brown university</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>colorado school of mines</td>
      <td>colorado school of mines</td>
      <td>1.000000</td>
      <td>colorado school of mines</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



- **Filtering Matches**: We focus on matches with a Jaro-Winkler score of 0.975 or higher to ensure high confidence.
- **Merging Datasets**: The filtered matches are merged with the IPEDS dataset to verify and enhance the match rate.

## Further Standardizing School Names with LLM

To achieve even greater accuracy, we use a Large Language Model (LLM) to standardize the spelling of school names. This step helps eliminate minor discrepancies that could affect the match rate:


```python
def extract_standard(school_list,
                     user_model):
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    standardized_schools = []
    
    for school in school_list:
        prompt = f"""Please provide me with the correct and standard way of spelling the following college in triple backtics: ```{school}``` \
        put your response in JSON format with 'school' as the key and your output as the value."""
        try:
            response = client.chat.completions.create(
                model=user_model,
                response_format={"type": "json_object"},
                messages=[
                    {
                      "role": "system",
                      "content": f"""You provide direct and concise responses and provide only the answer to the question asked. \
                      You avoid using terms like, 'the standard way to spell this school is...' and provide only the standard way to spell the school."""
                    },
                    {'role': 'user', 
                     'content': prompt}
                ],
                temperature=0
            )


            standardized_school = response.choices[0].message.content
            standardized_schools.append(standardized_school)
            print(f"Processing row {school}")
        except Exception as e:
            print(f"An error occurred: {e}")
            standardized_schools.append(f"Error processing input: {school}")
            print('error tho')
            
    data = []
    
    for item in standardized_schools:
        parsed_json = json.loads(item)
        data.append(parsed_json)
        
    df = pd.DataFrame(data)
    standardized_schools = df['school']
    
    return standardized_schools
```
LLM Standardization: The function queries GPT to provide the standard spelling for each school name, formatted in JSON.
Error Handling: The function includes error handling to manage any issues during the API call.


## Leveraging GPT-3 for Enhanced Standardization

To further refine our data matching process, we utilize GPT-3 to standardize the spelling of school names across both datasets. This step aims to reduce discrepancies caused by variations in naming conventions and improve the overall match rate. We use GPT3 because of the lower cost and relative simplicity of this task.

We apply the `extract_standard` function to both the Berkeley and IPEDS datasets using GPT-3. This function queries GPT-3 to provide a consistent and standardized spelling for each school name:

```python
berkeley_schools['gpt3_standardized'] = extract_standard(berkeley_schools['school'],
                                                          GPT_3)

berkeley_schools.head()
```


```python
iped_schools['gpt3_standardized'] = extract_standard(iped_schools['school'],
                                                          GPT_3)
```
With standardized names in place, we perform another round of matching using the Jaro-Winkler algorithm, this time on the GPT-3 standardized columns.

The table below shows a sample of the results after applying GPT-3 standardization and matching:

```python
matches_gpt = berkeley_schools['gpt3_standardized'].apply(lambda x: find_best_match(x, iped_schools['gpt3_standardized']))

berkeley_schools['Best Match GPT'] = matches_gpt.apply(lambda x: x[0])
berkeley_schools['Match Score GPT'] = matches_gpt.apply(lambda x: x[1])

berkeley_schools.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>Best Match</th>
      <th>Match Score</th>
      <th>country</th>
      <th>domestic</th>
      <th>gpt3_standardized</th>
      <th>Best Match GPT</th>
      <th>Match Score GPT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Kentucky</td>
      <td>University of Kentucky</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>technionisrael inst of tech</td>
      <td>None</td>
      <td>0.828889</td>
      <td>Israel</td>
      <td>0</td>
      <td>Technion Israel Institute of Technology</td>
      <td>None</td>
      <td>0.806527</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Minnesota Twin Cities</td>
      <td>University of Minnesota Twin Cities</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>univ of nairobi</td>
      <td>None</td>
      <td>0.857179</td>
      <td>Kenya</td>
      <td>0</td>
      <td>University of Nairobi</td>
      <td>None</td>
      <td>0.931746</td>
    </tr>
    <tr>
      <th>4</th>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Southern California</td>
      <td>University of Southern California</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>


## Evaluating the True Match Rate

After leveraging GPT-3 for standardization and applying the Jaro-Winkler algorithm, we achieved a match rate of 31.32%. However, this calculation used the total number of schools in the Berkeley dataset as the denominator, which includes international entries. To obtain a more accurate match rate, we need to focus on domestic schools only.

We previously asked GPT to identify whether each school in the Berkeley dataset is located in the United States. Now, we use this information to refine our denominator and calculate the true match rate:

```python
filtered_matches_gpt = berkeley_schools[berkeley_schools['Match Score GPT'] >= 0.975]

merged_3 = filtered_matches_gpt.merge(iped_schools, left_on='Best Match GPT', right_on='gpt3_standardized', suffixes=('_left', '_right'), how='left')
merged_3.head()
```

- **Domestic Focus**: By using only domestic schools as the denominator, we ensure that our match rate reflects the relevant subset of data.
- **Accurate Denominator**: GPT identified 2,409 domestic schools, which serves as the new denominator for calculating the match rate.


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school_left</th>
      <th>Best Match</th>
      <th>Match Score</th>
      <th>country</th>
      <th>domestic</th>
      <th>gpt3_standardized_left</th>
      <th>Best Match GPT</th>
      <th>Match Score GPT</th>
      <th>school_right</th>
      <th>match</th>
      <th>gpt3_standardized_right</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Kentucky</td>
      <td>University of Kentucky</td>
      <td>1.0</td>
      <td>university of kentucky</td>
      <td>1</td>
      <td>University of Kentucky</td>
    </tr>
    <tr>
      <th>1</th>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Minnesota Twin Cities</td>
      <td>University of Minnesota Twin Cities</td>
      <td>1.0</td>
      <td>university of minnesotatwin cities</td>
      <td>1</td>
      <td>University of Minnesota Twin Cities</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Southern California</td>
      <td>University of Southern California</td>
      <td>1.0</td>
      <td>university of southern california</td>
      <td>1</td>
      <td>University of Southern California</td>
    </tr>
    <tr>
      <th>3</th>
      <td>brown university</td>
      <td>brown university</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>Brown University</td>
      <td>Brown University</td>
      <td>1.0</td>
      <td>brown university</td>
      <td>1</td>
      <td>Brown University</td>
    </tr>
    <tr>
      <th>4</th>
      <td>colorado school of mines</td>
      <td>colorado school of mines</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>Colorado School of Mines</td>
      <td>Colorado School of Mines</td>
      <td>1.0</td>
      <td>colorado school of mines</td>
      <td>1</td>
      <td>Colorado School of Mines</td>
    </tr>
  </tbody>
</table>
</div>


## Final Match Rate Calculation
With the refined denominator, we can now calculate the true match rate for domestic schools:

```python
print(f"The match rate with standardizing strings and a jaro-winkler threshold of .975 is {merged_3['match'].sum() / highest_possible_match * 100:.2f}%")
```

    The match rate with standardizing strings and a jaro-winkler threshold of .975 is 31.32%

- **True Match Rate**: This calculation provides a more accurate representation of our data matching success, focusing on schools located in the United States.

```python
berkeley_schools.to_csv('data/berkeley_schools_features.csv', index = False)
iped_schools.to_csv('data/IPEDS_schools_features.csv', index = False)
```

The match rate is still not very high. But, the right-side data (IPEDS) only contains data on schools from the US, therefore using the total school denominator from the left-side data (Berkeley) is adequate. Recall, earlier we asked GPT to identify whether the school was located in the US. Let's take only those rows where the school is domestic and use that as the denominator and see what the true match rate is.


```python
true_highest_possible_match = berkeley_schools['domestic'].sum()
print(f"GPT identified {true_highest_possible_match} domestic schools. This should be our denominator.")
```

    GPT identified 2409 domestic schools. This should be our denominator.


Below we find that we are now able to get a 67.16% thanks to GPT and jaro-winkler matching
```python
print(f"The match rate with standardizing strings of domestic schools and a jaro-winkler threshold of .975 is {merged_3['match'].sum() / true_highest_possible_match * 100:.2f}%")
```

    The match rate with standardizing strings of domestic schools and a jaro-winkler threshold of .975 is 67.16%


For my own exploration, here's a list of the domestic schools that I wasn't able to match


```python
non_matches = berkeley_schools[berkeley_schools['domestic'] == 1]
non_matches = non_matches[non_matches['Match Score GPT'] < 0.975]
```


```python
non_matches.to_csv('data/berkeley_ipeds_non_matches.csv', index=False)
```

Below, I'm producing a final matched dataset for manual inspection

```python
berkeley_baselines = pd.read_excel('data/berkeley_schools.xlsx')
berkeley_baselines = berkeley_baselines[['UG Degree School']]
print(len(berkeley_baselines))
berkeley_baselines.head()
```

    158007





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>UG Degree School</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>University of Kentucky</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Technion-Israel Inst of Tech</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Minnesota, Twin Cities</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Univ of Nairobi</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Southern California</td>
    </tr>
  </tbody>
</table>
</div>




```python
berkeley_baselines = pd.DataFrame(berkeley_baselines['UG Degree School'].dropna().unique(), columns=['UG Degree School'])
berkeley_baselines['school_left'] = berkeley_baselines['UG Degree School']
berkeley_baselines = clean_school_names(berkeley_baselines, 'school_left')

print(len(berkeley_baselines))
berkeley_baselines.head()
```

    5929





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>UG Degree School</th>
      <th>school_left</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>University of Kentucky</td>
      <td>university of kentucky</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Technion-Israel Inst of Tech</td>
      <td>technionisrael inst of tech</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Minnesota, Twin Cities</td>
      <td>university of minnesota twin cities</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Univ of Nairobi</td>
      <td>univ of nairobi</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Southern California</td>
      <td>university of southern california</td>
    </tr>
  </tbody>
</table>
</div>




```python
berkeley_schools = pd.read_csv('data/berkeley_schools_features.csv')
```


```python
merged_final = berkeley_schools.merge(
    iped_schools, 
    left_on='Best Match GPT', 
    right_on='gpt3_standardized', 
    suffixes=('_left', '_right'), 
    how='left'
)

print(len(merged_final))
merged_final.head()
```

    5186





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school_left</th>
      <th>Best Match</th>
      <th>Match Score</th>
      <th>country</th>
      <th>domestic</th>
      <th>gpt3_standardized_left</th>
      <th>Best Match GPT</th>
      <th>Match Score GPT</th>
      <th>school_right</th>
      <th>match</th>
      <th>gpt3_standardized_right</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Kentucky</td>
      <td>University of Kentucky</td>
      <td>1.000000</td>
      <td>university of kentucky</td>
      <td>1.0</td>
      <td>University of Kentucky</td>
    </tr>
    <tr>
      <th>1</th>
      <td>technionisrael inst of tech</td>
      <td>None</td>
      <td>0.828889</td>
      <td>Israel</td>
      <td>0</td>
      <td>Technion Israel Institute of Technology</td>
      <td>None</td>
      <td>0.806527</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Minnesota Twin Cities</td>
      <td>University of Minnesota Twin Cities</td>
      <td>1.000000</td>
      <td>university of minnesotatwin cities</td>
      <td>1.0</td>
      <td>University of Minnesota Twin Cities</td>
    </tr>
    <tr>
      <th>3</th>
      <td>univ of nairobi</td>
      <td>None</td>
      <td>0.857179</td>
      <td>Kenya</td>
      <td>0</td>
      <td>University of Nairobi</td>
      <td>None</td>
      <td>0.931746</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Southern California</td>
      <td>University of Southern California</td>
      <td>1.000000</td>
      <td>university of southern california</td>
      <td>1.0</td>
      <td>University of Southern California</td>
    </tr>
  </tbody>
</table>
</div>




```python
merged_final = berkeley_baselines.merge(merged_final, on= 'school_left', how = 'left')

print(len(merged_final))
merged_final.head()
```

    5957





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>UG Degree School</th>
      <th>school_left</th>
      <th>Best Match</th>
      <th>Match Score</th>
      <th>country</th>
      <th>domestic</th>
      <th>gpt3_standardized_left</th>
      <th>Best Match GPT</th>
      <th>Match Score GPT</th>
      <th>school_right</th>
      <th>match</th>
      <th>gpt3_standardized_right</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>University of Kentucky</td>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Kentucky</td>
      <td>University of Kentucky</td>
      <td>1.000000</td>
      <td>university of kentucky</td>
      <td>1.0</td>
      <td>University of Kentucky</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Technion-Israel Inst of Tech</td>
      <td>technionisrael inst of tech</td>
      <td>None</td>
      <td>0.828889</td>
      <td>Israel</td>
      <td>0</td>
      <td>Technion Israel Institute of Technology</td>
      <td>None</td>
      <td>0.806527</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Minnesota, Twin Cities</td>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Minnesota Twin Cities</td>
      <td>University of Minnesota Twin Cities</td>
      <td>1.000000</td>
      <td>university of minnesotatwin cities</td>
      <td>1.0</td>
      <td>University of Minnesota Twin Cities</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Univ of Nairobi</td>
      <td>univ of nairobi</td>
      <td>None</td>
      <td>0.857179</td>
      <td>Kenya</td>
      <td>0</td>
      <td>University of Nairobi</td>
      <td>None</td>
      <td>0.931746</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Southern California</td>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Southern California</td>
      <td>University of Southern California</td>
      <td>1.000000</td>
      <td>university of southern california</td>
      <td>1.0</td>
      <td>University of Southern California</td>
    </tr>
  </tbody>
</table>
</div>




```python
iped_baselines = pd.read_csv('data/IPEDS_schools.csv')
iped_baselines = iped_baselines[['INSTNM','OPEID','OPEID6']]
iped_baselines['school_right'] = iped_baselines['INSTNM']

iped_baselines = clean_school_names(iped_baselines, 'school_right')

iped_baselines.head()
```

    /var/folders/89/6bdxzk2j30v5n3wstywbcpg80000gn/T/ipykernel_17234/917143819.py:1: DtypeWarning: Columns (9,1537,1540,1542,1606,1608,1614,1615,1619,1620,1621,1622,1623,1624,1625,1626,1627,1628,1629,1703,1704,1725,1726,1727,1728,1729,1743,1815,1816,1817,1818,1823,1824,1830,1831,1879,1880,1881,1882,1883,1884,1885,1886,1887,1888,1889,1890,1891,1892,1893,1894,1895,1896,1897,1898,1909,1910,1911,1912,1913,1957,1958,1959,1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1983,1984,2376,2377,2403,2404,2495,2496,2497,2498,2499,2500,2501,2502,2503,2504,2505,2506,2507,2508,2509,2510,2511,2512,2513,2514,2515,2516,2517,2518,2519,2520,2521,2522,2523,2524,2525,2526,2527,2528,2529,2530,2958) have mixed types. Specify dtype option on import or set low_memory=False.
      iped_baselines = pd.read_csv('data/IPEDS_schools.csv')





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>INSTNM</th>
      <th>OPEID</th>
      <th>OPEID6</th>
      <th>school_right</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Alabama A &amp; M University</td>
      <td>100200.0</td>
      <td>1002.0</td>
      <td>alabama a &amp; m university</td>
    </tr>
    <tr>
      <th>1</th>
      <td>University of Alabama at Birmingham</td>
      <td>105200.0</td>
      <td>1052.0</td>
      <td>university of alabama at birmingham</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Amridge University</td>
      <td>2503400.0</td>
      <td>25034.0</td>
      <td>amridge university</td>
    </tr>
    <tr>
      <th>3</th>
      <td>University of Alabama in Huntsville</td>
      <td>105500.0</td>
      <td>1055.0</td>
      <td>university of alabama in huntsville</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Alabama State University</td>
      <td>100500.0</td>
      <td>1005.0</td>
      <td>alabama state university</td>
    </tr>
  </tbody>
</table>
</div>




```python
merged_final['school_right'] = merged_final.apply(lambda row: np.nan if row['Match Score GPT'] < 0.975 else row['school_right'], axis=1)

merged_final = merged_final.merge(iped_baselines, on= 'school_right', how = 'left')

merged_final.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>UG Degree School</th>
      <th>school_left</th>
      <th>Best Match</th>
      <th>Match Score</th>
      <th>country</th>
      <th>domestic</th>
      <th>gpt3_standardized_left</th>
      <th>Best Match GPT</th>
      <th>Match Score GPT</th>
      <th>school_right</th>
      <th>match</th>
      <th>gpt3_standardized_right</th>
      <th>INSTNM</th>
      <th>OPEID</th>
      <th>OPEID6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>University of Kentucky</td>
      <td>university of kentucky</td>
      <td>university of kentucky</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Kentucky</td>
      <td>University of Kentucky</td>
      <td>1.000000</td>
      <td>university of kentucky</td>
      <td>1.0</td>
      <td>University of Kentucky</td>
      <td>University of Kentucky</td>
      <td>198900.0</td>
      <td>1989.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Technion-Israel Inst of Tech</td>
      <td>technionisrael inst of tech</td>
      <td>None</td>
      <td>0.828889</td>
      <td>Israel</td>
      <td>0</td>
      <td>Technion Israel Institute of Technology</td>
      <td>None</td>
      <td>0.806527</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Minnesota, Twin Cities</td>
      <td>university of minnesota twin cities</td>
      <td>university of minnesotatwin cities</td>
      <td>0.982521</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Minnesota Twin Cities</td>
      <td>University of Minnesota Twin Cities</td>
      <td>1.000000</td>
      <td>university of minnesotatwin cities</td>
      <td>1.0</td>
      <td>University of Minnesota Twin Cities</td>
      <td>University of Minnesota-Twin Cities</td>
      <td>396900.0</td>
      <td>3969.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Univ of Nairobi</td>
      <td>univ of nairobi</td>
      <td>None</td>
      <td>0.857179</td>
      <td>Kenya</td>
      <td>0</td>
      <td>University of Nairobi</td>
      <td>None</td>
      <td>0.931746</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Southern California</td>
      <td>university of southern california</td>
      <td>university of southern california</td>
      <td>1.000000</td>
      <td>United States</td>
      <td>1</td>
      <td>University of Southern California</td>
      <td>University of Southern California</td>
      <td>1.000000</td>
      <td>university of southern california</td>
      <td>1.0</td>
      <td>University of Southern California</td>
      <td>University of Southern California</td>
      <td>132800.0</td>
      <td>1328.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
columns_to_keep = ['UG Degree School' ,'gpt3_standardized_left', 'INSTNM', 'OPEID', 'OPEID6', 'country', 'domestic']

schools_matched = merged_final[columns_to_keep].rename(columns={
    'UG Degree School': 'Berkeley School Name',
    'INSTNM': 'IPEDS School Name',
    'gpt3_standardized_left': 'Berkeley Correct School Name',
    'country': 'Estimated Country',
    'domestic': 'Estimated Domestic'
})

schools_matched['Estimated Country'] = schools_matched.apply(
    lambda row: 'United States' if pd.notna(row['OPEID']) else row['Estimated Country'], axis=1
)
schools_matched['Estimated Domestic'] = schools_matched.apply(
    lambda row: 1 if pd.notna(row['OPEID']) else row['Estimated Domestic'], axis=1
)

schools_matched.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Berkeley School Name</th>
      <th>Berkeley Correct School Name</th>
      <th>IPEDS School Name</th>
      <th>OPEID</th>
      <th>OPEID6</th>
      <th>Estimated Country</th>
      <th>Estimated Domestic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>University of Kentucky</td>
      <td>University of Kentucky</td>
      <td>University of Kentucky</td>
      <td>198900.0</td>
      <td>1989.0</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Technion-Israel Inst of Tech</td>
      <td>Technion Israel Institute of Technology</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Israel</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Minnesota, Twin Cities</td>
      <td>University of Minnesota Twin Cities</td>
      <td>University of Minnesota-Twin Cities</td>
      <td>396900.0</td>
      <td>3969.0</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Univ of Nairobi</td>
      <td>University of Nairobi</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Kenya</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Southern California</td>
      <td>University of Southern California</td>
      <td>University of Southern California</td>
      <td>132800.0</td>
      <td>1328.0</td>
      <td>United States</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
schools_matched.to_csv('data/berkeley_ipeds_matches.csv', index=False)
```
