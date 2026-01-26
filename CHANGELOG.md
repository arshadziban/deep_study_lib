# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2026-01-27

### Removed
- Removed `summary()` method from Report class
- Console summary output no longer displayed after saving reports

## [1.0.1] - 2026-01-26

### Fixed
- Fixed matplotlib backend compatibility issue with Jupyter notebooks
- `matplotlib.use('Agg')` now gracefully handles pre-configured backends

## [1.0.0] - 2026-01-26

### Added
- Initial release of Deep Study package
- Dataset overview and summary statistics
- Feature profiling with detailed statistics
- Target variable analysis
- Feature importance using Random Forest
- Professional HTML report generation
- Jupyter notebook integration with iframe rendering
- Large number formatting (K, M, B suffixes)
- Distribution visualizations for numeric and categorical features
- Missing value analysis
- Memory usage tracking

### Features
- `Analyzer` class for easy data analysis
- `Report` class with HTML rendering
- Support for CSV and Excel file loading
- Customizable target variable analysis
