# Shark Attack Dataset Analysis

📓 [Jupyter Notebook](Shark_Attacks.ipynb)
📊 [View Project Slides](https://docs.google.com/presentation/d/1S4-Dp7hUE5fuvDM1wnxrG_bx-HsWqrsjZrHfotUjU5c/edit?usp=sharing)
🦈 [Original Dataset](https://www.sharkattackfile.net/)

## Project Overview

This project explores a global shark attack dataset using Python for data cleaning, transformation, and exploratory data analysis (EDA).

The goal of the project was to identify demographic, geographic, behavioral, and seasonal patterns associated with shark attack incidents.

---

# Data Cleaning

Several cleaning steps were performed to improve data consistency and prepare the dataset for analysis.

### Cleaning Tasks

- Removed unnecessary columns and duplicate information
- Standardized column names
- Cleaned text formatting and whitespace
- Standardized country names and grouped invalid values into `"other"`
- Categorized activities using regex pattern matching:
  - swimming
  - boarding / surfing
  - fishing
  - diving
- Standardized sex values into:
  - `M`
  - `F`
  - `unknown`
- Cleaned age values by extracting numeric ages and handling invalid entries
- Cleaned and standardized date values using regex and datetime parsing
- Converted valid dates into datetime format while handling invalid dates as `NaT`

---

# Exploratory Data Analysis (EDA)

The analysis focused on identifying patterns across:

- activity
- country
- sex
- age
- seasonality
- time trends

### Visualizations Included

- bar charts
- stacked bar charts
- histograms
- stacked histograms
- seasonal trend plots
- country comparison plots
- heatmaps

---

# Key Findings

## Geographic Patterns

- The United States, Australia, and South Africa reported the highest number of shark attacks.
- English-speaking countries dominated the dataset, suggesting possible reporting or collection bias.
- Focusing on the top 3–4 countries would likely provide the highest business or marketing impact.

---

## Activity Patterns

- Surfing, paddleboarding, boogie boarding, swimming, snorkeling, and bathing were among the highest-risk activities.
- Results suggest potential demand for shark-deterrent products targeting both board sports and swimwear users.

---

## Demographic Patterns

- Shark attacks were heavily skewed toward male victims.
- Males experienced more surfing- and fishing-related attacks.
- Swimming-related attacks were proportionally more common among women.
- Younger individuals appeared to face higher shark attack risk across both sexes.

---

## Seasonal Patterns

- Shark attacks peaked during local summer seasons.
- Southern Hemisphere countries peaked during:
  - December–February
- Northern Hemisphere countries peaked during:
  - June–September
- Seasonal trends suggest that attack frequency may be strongly associated with increased human ocean activity during warmer months.

---

# Technologies Used

- Python
- pandas
- numpy
- seaborn
- matplotlib
- regex

---

# Conclusion

The analysis revealed strong relationships between shark attacks and:

- recreational ocean activities
- demographic factors
- geographic location
- seasonal human behavior

Overall, the project demonstrates how data cleaning and exploratory analysis can uncover meaningful patterns in real-world datasets.
