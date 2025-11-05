# Solow Growth Model Analysis

## Overview
This project analyzes Penn World Table data using Python and Stata to compute Solow model variables, clean data, generate summary statistics, and create graphs.

## Folder Structure
- `data/raw/`: Original PWT data
- `data/cleaned/`: Cleaned and transformed datasets
- `graphs/`: Output graphs
- `scripts/`: Python and Stata scripts
- `STATA/` : Stata .do files
- `Python/` : Python .py file

## Codes
-"Data_cleaning.do": Cleans the data and removes irrelevant columns and add new ones.
-"Data_analysis.do" : Do some basic data analysis such as descriptive stats and some graphs
- "Data_analysis.py" : Do real analysis and data prep with solow model.

## How to Reproduce
1. Clone the repo: `git clone https://github.com/M-Peter9/Coding_assignment`
2. Install Python packages: `pip install pandas matplotlib seaborn openpyxl`
3. Run the Python script: `python Data_analysis.py`
4. Run the Stata `.do` files in order
5. Outputs will be saved in `data/cleaned/` and `graphs/`

## Dependencies
- Python 3.11+
- pandas, seaborn, matplotlib, openpyxl
- Stata 17+

## Author
Péter Márton
