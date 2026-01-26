# profiler module - Feature profiling for detailed statistics
"""
Feature Profiler: Generates detailed statistics for each feature
similar to pandas-profiling but lightweight.
"""

import pandas as pd
import numpy as np
from collections import Counter


def profile_feature(series, name):
    """Generate detailed profile for a single feature."""
    profile = {
        "name": name,
        "dtype": str(series.dtype),
        "count": len(series),
        "missing": series.isna().sum(),
        "missing_pct": round(series.isna().sum() / len(series) * 100, 2),
        "distinct": series.nunique(),
        "distinct_pct": round(series.nunique() / len(series) * 100, 2),
        "memory_kb": round(series.memory_usage(deep=True) / 1024, 2),
    }
    
    # Determine feature type
    if pd.api.types.is_numeric_dtype(series):
        profile["type"] = "Numeric"
        profile.update(_numeric_stats(series))
    elif pd.api.types.is_datetime64_any_dtype(series):
        profile["type"] = "DateTime"
        profile.update(_datetime_stats(series))
    else:
        profile["type"] = "Categorical"
        profile.update(_categorical_stats(series))
    
    return profile


def _format_number(num):
    """Format large numbers for display."""
    if num is None:
        return "N/A"
    try:
        num = float(num)
        if abs(num) >= 1_000_000_000:
            return f"{num/1_000_000_000:.2f}B"
        elif abs(num) >= 1_000_000:
            return f"{num/1_000_000:.2f}M"
        elif abs(num) >= 1_000:
            return f"{num/1_000:.2f}K"
        elif abs(num) < 1 and num != 0:
            return f"{num:.4f}"
        else:
            return f"{num:,.2f}"
    except:
        return str(num)


def _numeric_stats(series):
    """Statistics for numeric features."""
    clean = series.dropna()
    
    mean_val = clean.mean() if len(clean) > 0 else None
    min_val = clean.min() if len(clean) > 0 else None
    max_val = clean.max() if len(clean) > 0 else None
    
    stats = {
        "mean": _format_number(mean_val),
        "std": round(clean.std(), 4) if len(clean) > 0 else None,
        "min": _format_number(min_val),
        "max": _format_number(max_val),
        "median": clean.median() if len(clean) > 0 else None,
        "q1": clean.quantile(0.25) if len(clean) > 0 else None,
        "q3": clean.quantile(0.75) if len(clean) > 0 else None,
        "zeros": (clean == 0).sum(),
        "zeros_pct": round((clean == 0).sum() / len(clean) * 100, 2) if len(clean) > 0 else 0,
        "negative": (clean < 0).sum(),
    }
    
    # Distribution histogram data (10 bins)
    if len(clean) > 0:
        hist, bin_edges = np.histogram(clean, bins=10)
        stats["histogram"] = {
            "counts": hist.tolist(),
            "edges": [round(e, 2) for e in bin_edges.tolist()]
        }
    
    return stats


def _categorical_stats(series):
    """Statistics for categorical features."""
    clean = series.dropna().astype(str)
    value_counts = clean.value_counts()
    
    stats = {
        "top_values": [],
        "mode": value_counts.index[0] if len(value_counts) > 0 else None,
        "mode_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
    }
    
    # Top 10 values with counts and percentages
    for val, count in value_counts.head(10).items():
        stats["top_values"].append({
            "value": str(val),
            "count": int(count),
            "pct": round(count / len(clean) * 100, 2) if len(clean) > 0 else 0
        })
    
    return stats


def _datetime_stats(series):
    """Statistics for datetime features."""
    clean = series.dropna()
    stats = {
        "min_date": str(clean.min()) if len(clean) > 0 else None,
        "max_date": str(clean.max()) if len(clean) > 0 else None,
        "range_days": (clean.max() - clean.min()).days if len(clean) > 0 else None,
    }
    return stats


def profile_dataframe(df):
    """Generate profiles for all features in a DataFrame."""
    profiles = []
    for col in df.columns:
        profiles.append(profile_feature(df[col], col))
    return profiles


def profile_correlations_with_target(df, target, correlations):
    """
    Create correlation summary with target for all features.
    Returns list of dicts with feature name, type, and correlation score.
    """
    results = []
    for col in df.columns:
        if col == target:
            continue
        
        corr_score = correlations.get(col, 0)
        
        # Determine correlation strength
        abs_corr = abs(corr_score)
        if abs_corr >= 0.5:
            strength = "Strong"
        elif abs_corr >= 0.3:
            strength = "Moderate"
        elif abs_corr >= 0.1:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        results.append({
            "feature": col,
            "type": str(df[col].dtype),
            "correlation": round(corr_score, 4),
            "strength": strength
        })
    
    # Sort by absolute correlation value
    results.sort(key=lambda x: abs(x["correlation"]), reverse=True)
    return results
