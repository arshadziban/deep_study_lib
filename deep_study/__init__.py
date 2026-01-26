# deep_study package
"""
Deep Study - Dataset Overview and Feature Analysis

A lightweight Python package for automated exploratory data analysis,
featuring detailed feature profiling and analysis with target variables.

Example:
    >>> from deep_study import Analyzer
    >>> analyzer = Analyzer(df, target="target_column")
    >>> report = analyzer.run()
    >>> report.save_html("deep_study_report.html")
"""

__version__ = "1.0.3"
__author__ = "Shah Md. Arshad Rahman Ziban"

from .analyzer import Analyzer
from .report import Report
from .profiler import profile_dataframe, profile_feature

__all__ = ["Analyzer", "Report", "profile_dataframe", "profile_feature"]