import pandas as pd

def load_data(data):
    if isinstance(data, str):
        if data.endswith(".csv"):
            return pd.read_csv(data)
        elif data.endswith(".xlsx"):
            return pd.read_excel(data)
        else:
            raise ValueError("Unsupported file format")
    return data.copy()
