# analysis module
from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)

def feature_importance(df, target, target_type):
    X = df.drop(columns=[target])
    y = df[target]

    if target_type == "numeric":
        model = RandomForestRegressor(
            n_estimators=100, random_state=42
        )
    else:
        model = RandomForestClassifier(
            n_estimators=100, random_state=42
        )

    model.fit(X, y)

    return dict(
        sorted(
            zip(X.columns, model.feature_importances_),
            key=lambda x: x[1],
            reverse=True
        )
    )
