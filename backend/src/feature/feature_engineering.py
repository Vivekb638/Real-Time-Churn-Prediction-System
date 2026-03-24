
import pandas as pd

def feature_engineering(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()

    # Safety
    X["tenure"] = pd.to_numeric(X["tenure"], errors="coerce").fillna(0)
    X["MonthlyCharges"] = pd.to_numeric(X["MonthlyCharges"], errors="coerce").fillna(0)
    X["TotalCharges"] = pd.to_numeric(X["TotalCharges"], errors="coerce").fillna(0)

    # Feature 1: charge per tenure
    X["charge_per_tenure"] = X["MonthlyCharges"] / (X["tenure"] + 1)

    # Feature 2: number of services
    services = [
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    X["num_services"] = (X[services] == "Yes").sum(axis=1)

    # Feature 3: tenure group
    X["tenure_group"] = pd.cut(
        X["tenure"],
        bins=[0, 12, 24, 48, 72],
        labels=["0-1yr", "1-2yr", "2-4yr", "4-6yr"],
        include_lowest=True
    )

    return X
