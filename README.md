# HR Data Wrangling & Standardization Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458)
![Status](https://img.shields.io/badge/Status-Completed-success)

## Project Overview
This project demonstrates an **end-to-end data cleaning pipeline** designed to process a messy, synthetic Human Resources dataset (~2,500 records). 

The goal was to transform raw, inconsistent data—mimicking real-world legacy system exports—into a structured, analysis-ready format. The project focuses on handling mixed data types, string parsing, regex pattern matching, and complex categorical mapping.

## Key Challenges & Solutions
The dataset contained intentional errors often found in enterprise data. Here is how they were handled:

| Challenge | Raw Data Example  | Solution  | Cleaned Data Example |
| :--- | :--- | :--- | :--- |
| **Inconsistent Dates** | `2023.05.12`, `12/05/2023`, `Pending` | **Custom Parser:** `try/except` logic for multi-format parsing | `2023-05-12` |
| **Mixed Currencies** | `$120k`, `120,000 USD`, `85000` | **String Cleaning:** Removed symbols, multiplied 'k', cast to float | `120000.0` |
| **Dirty Text (Lists)** | `Java; Excell / Python` | **Explode/Implode:** Split delimiters, exploded rows, mapped typos | `['Java', 'Excel', 'Python']` |
| **Phone/SSN** | `+1 (555) 123.4567` | **Regex:** Removed country codes, enforced standard separators | `555-123-4567` |
| **Typos** | `Enginering`, `Mktg` | **Dictionary Mapping:** Standardized categorical values | `Engineering`, `Marketing` |

##  Tech Stack & Techniques
* **Python 3.x**
* **Pandas:** `explode()`, `groupby()`, `apply()`, `Vectorized String Operations`
* **Regular Expressions (Regex):** Pattern matching for phone numbers and SSN validation.
* **NumPy:** Efficient handling of `NaN` and numerical operations.

##  Code Highlights

### 1. Advanced List Handling (Explode & Clean)
Cleaning comma-separated values inside a single cell is tricky. I used the `explode` method to treat each skill individually, fixed typos, and regrouped them.

```python
# Unifying separators and splitting into lists
df["Skills"] = df["Skills"].str.replace(";", ",").str.replace("/", ",")
df["Skills"] = df["Skills"].str.split(",")

# Exploding to clean individual elements (e.g., "Excell" -> "Excel")
df_exploded = df.explode("Skills")
df_exploded["Skills"] = df_exploded["Skills"].str.strip().replace(skills_mapping)

# Grouping back to list
df["Skills"] = df_exploded.groupby(level=0)["Skills"].agg(list)
2. Robust Date Parsing
Instead of relying on simple casting, I implemented a robust function to handle multiple date formats and gracefully handle errors.

Python

def clean_date_data(data_str):
    formats_to_try = ["%Y-%m-%d", "%m/%d/%Y", "%d.%m.%Y"]
    for fmt in formats_to_try:
        try:
            return datetime.strptime(data_str.strip(), fmt)
        except ValueError:
            continue
    return pd.NaT # Handle "Pending" or invalid dates
3. Regex for Phone Normalization
A two-step regex process to standardize phone numbers from +1 (555) 123.4567 to 555-123-4567.

Python

# Step 1: Remove country code (+1) and parentheses
df["Phone"] = df["Phone"].str.replace(r'\+1\s|[\(\)]', '', regex=True)

# Step 2: Replace dots and spaces with hyphens
df["Phone"] = df["Phone"].str.replace(r'[ .]+', '-', regex=True)
```

## Results
The final output is a clean CSV file (cleaned_hr_data.csv) ready for visualization tools like Tableau, PowerBI, or further Python analysis.

Rows: ~2,500

Columns: 13 (Standardized)

Data Quality: 100% valid formats for Dates, Salaries, and Categorical fields.


### Created by Marta Golka - Data Analyst / Python Developer
