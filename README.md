# Deep Study

**Automated Dataset Overview and Feature Analysis for Data Science**

Deep Study is a lightweight Python package for automated exploratory data analysis (EDA), featuring detailed feature profiling and analysis with target variables. Generate professional HTML reports with just a few lines of code.

[![PyPI version](https://badge.fury.io/py/deep-study.svg)](https://badge.fury.io/py/deep-study)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Feature Profiling**: Detailed statistics for each feature (distinct values, missing values, distribution, memory usage)
- **Target Analysis**: Automatic analysis of feature relationships with target variable
- **Feature Importance**: ML-based feature importance using Random Forest
- **Beautiful Reports**: Generate professional HTML reports with visualizations
- **Jupyter Integration**: Reports render beautifully in Jupyter notebooks
- **Easy to Use**: Simple API - just 3 lines of code to generate a complete analysis

## Installation

```bash
pip install deep-study
```

Or install from source:

```bash
git clone https://github.com/arshadziban/deep_study_lib.git
cd deep_study_lib
pip install -e .
```

## Quick Start

```python
from deep_study import Analyzer

# Create analyzer with your data
analyzer = Analyzer(df, target="target_column")

# Run analysis
report = analyzer.run()

# Show output
report
```

## Report Contents

The generated HTML report includes:

### 1. Dataset Summary
- Total rows and columns
- Target variable information
- Overall dataset statistics

### 2. Individual Feature Profiles
For each feature in your dataset:
- **Type**: Numeric, Categorical, or DateTime
- **Distinct Values**: Count and percentage
- **Missing Values**: Count and percentage  
- **Memory Usage**: Efficient memory tracking
- **Distribution Visualization**: Histograms for numeric, bar charts for categorical
- **Statistics**: Mean, min, max (with K/M/B formatting for large numbers)
- **Top Values**: Most frequent values for categorical features

## API Reference

### Analyzer

```python
from deep_study import Analyzer

analyzer = Analyzer(data, target)
```

**Parameters:**
- `data`: pandas DataFrame or path to CSV/Excel file
- `target`: Name of the target column

**Methods:**
- `run()`: Execute analysis and return Report object

### Report

**Methods:**
- `get_top_features(n)`: Get top N important features
- `get_feature_profile(name)`: Get profile for specific feature

## Example Output

```python
from deep_study import Analyzer
import pandas as pd

# Load your data
df = pd.read_csv("your_data.csv")

# Analyze
analyzer = Analyzer(df, target="outcome")
report = analyzer.run()

# Show output
report
```

## Requirements

- Python >= 3.8
- pandas >= 1.3.0
- numpy >= 1.20.0
- scikit-learn >= 1.0.0
- matplotlib >= 3.4.0
- jinja2 >= 3.0.0

## Author

**Shah Md. Arshad Rahman Ziban**

## Acknowledgments

- Built with pandas, scikit-learn, and matplotlib
- Inspired by the need for quick, professional data analysis reports
