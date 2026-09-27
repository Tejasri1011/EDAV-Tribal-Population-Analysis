Demographic Analysis of Tribal Population Data
Project Overview
This project analyzes tribal population data from selected states in India using Python. The dataset is cleaned, checked, and analyzed using NumPy, Pandas, Matplotlib, and Seaborn.
The analysis focuses on demographic indicators such as:
Population
Male and Female Population
Literacy Rate
Sex Ratio
Tribal distribution by Region and State
Tools and Libraries Used
Python
NumPy
Pandas
Matplotlib
Seaborn
Jupyter Notebook
Data Preparation
The Excel dataset was loaded using Pandas and checked using basic functions such as head(), columns, shape, and info().
The data preparation included:
Removing unnecessary header rows
Selecting the required Census records
Selecting the required columns
Renaming columns with meaningful names
Converting required columns to numeric values
Checking missing values
Checking duplicate records
Mapping state codes to state names
Mapping states to regions
Selecting records with Residence = Total
Calculating Literacy Rate
Calculating Sex Ratio
Performing basic validation checks
Analysis Performed
Q1: Population Statistics Using NumPy
NumPy was used to calculate:
Total population
Mean population
Minimum population
Maximum population
Standard deviation
Q2: Filter Tribes by Region
The data was grouped by Region and filtered using the regional median population. Tribes with population values above the regional median were selected and arranged using the following priority:
State
Population
Literacy Rate
Sex Ratio
Q3: Identify Missing Data and Apply Imputations
Missing values were identified using Pandas.
A missing Area_Name value was located and handled using the corresponding State_Code. A separate copy of the cleaned data was maintained for this missing-value handling step.
Duplicate values and other data consistency checks were also performed.
Q4: Group Data by Tribe and Region
he dataset was grouped using:
groupby(["Region", "Tribe"])
The number of records in each Region–Tribe group was also obtained using size().
Q5: Visualize Demographic Indicators
Seaborn and Matplotlib were used to create visualizations including:
Population and Literacy Rate by Region
Population vs Literacy Rate
Average Sex Ratio by Region
Literacy Rate Distribution by Region
Total Tribal Population by State
These visualizations help in understanding demographic patterns across the selected regions and states.
Conclusion
The project provides a basic demographic analysis of tribal population data using Python. The dataset was cleaned and validated before performing the analysis. NumPy was used for population statistics,
Pandas was used for filtering and grouping, and Seaborn and Matplotlib were used to visualize demographic indicators.
