# analyzer module
"""
AutoCorr Analyzer: Automated correlation and feature analysis.
"""

from .loader import load_data
from .preprocessing import (
    detect_column_types,
    handle_missing_values
)
from .encoding import encode_features
from .correlation import (
    compute_correlation,
    detect_target_type
)
from .analysis import feature_importance
from .profiler import profile_dataframe, profile_correlations_with_target
from .report import Report


class Analyzer:
    """
    Main analyzer class for automated feature analysis.
    
    Parameters
    ----------
    data : str or pd.DataFrame
        Path to CSV/Excel file or a pandas DataFrame
    target : str
        Name of the target column
    
    Example
    -------
    >>> analyzer = Analyzer(df, target="PHQ_class")
    >>> report = analyzer.run()
    >>> report.save_html("my_report.html")
    """
    
    def __init__(self, data, target):
        self.raw_df = load_data(data)
        self.df = self.raw_df.copy()
        self.target = target
        self._validate_target()
    
    def _validate_target(self):
        if self.target not in self.df.columns:
            raise ValueError(f"Target '{self.target}' not found in columns: {list(self.df.columns)}")
    
    def run(self):
        """
        Execute the full analysis pipeline.
        
        Returns
        -------
        Report
            Report object with analysis results
        """
        # Profile features before encoding (for raw statistics)
        feature_profiles = profile_dataframe(self.raw_df)
        
        # Detect and handle column types
        col_types = detect_column_types(self.df)
        handle_missing_values(self.df, col_types)
        encode_features(self.df, col_types, self.target)
        
        # Detect target type
        target_type = detect_target_type(self.df[self.target])
        
        # Compute correlations
        correlations = compute_correlation(
            self.df, self.target, target_type
        )
        
        # Compute feature importance
        importance = feature_importance(
            self.df, self.target, target_type
        )
        
        # Create correlation summary with target
        correlation_summary = profile_correlations_with_target(
            self.df, self.target, correlations
        )
        
        return Report(
            df=self.df,
            raw_df=self.raw_df,
            correlations=correlations,
            importance=importance,
            target=target_type,
            target_name=self.target,
            feature_profiles=feature_profiles,
            correlation_summary=correlation_summary
        )
