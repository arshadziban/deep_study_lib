# preprocessing module
import pandas as pd

def detect_column_types(df):
    types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            types[col] = "numeric"
        elif pd.api.types.is_bool_dtype(df[col]):
            types[col] = "boolean"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            types[col] = "datetime"
        else:
            types[col] = "categorical"
    return types


def handle_missing_values(df, col_types):
    for col, t in col_types.items():
        if t == "numeric":
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
