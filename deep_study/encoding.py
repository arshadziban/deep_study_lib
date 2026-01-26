# encoding module
from sklearn.preprocessing import LabelEncoder

def encode_features(df, col_types, target):
    encoders = {}

    for col, t in col_types.items():
        if col == target:
            continue

        if t == "categorical":
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le

        elif t == "boolean":
            df[col] = df[col].astype(int)

        elif t == "datetime":
            df[col] = df[col].astype("int64") // 10**9

    return encoders
