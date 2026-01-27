# correlation module
from sklearn.feature_selection import (
    mutual_info_regression,
    mutual_info_classif
)
import pandas as pd

def detect_target_type(series):
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    return "categorical"


def compute_correlation(df, target, target_type):
    X = df.drop(columns=[target])
    y = df[target]

    if target_type == "numeric":
        scores = mutual_info_regression(X, y)
    else:
        scores = mutual_info_classif(X, y)

    return dict(
        sorted(
            zip(X.columns, scores),
            key=lambda x: x[1],
            reverse=True
        )
    )
