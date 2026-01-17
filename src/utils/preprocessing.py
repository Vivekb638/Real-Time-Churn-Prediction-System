import pandas as pd

def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies all feature engineering steps required by the churn model.
    This function MUST be used everywhere: training, inference, batch, explainability.
    """

    df = df.copy()

    # ----------------------------
    # TYPE SAFETY & CLEANING
    # ----------------------------
    df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce").fillna(0)
    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce").fillna(0)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
    df["SeniorCitizen"] = pd.to_numeric(df["SeniorCitizen"], errors="coerce").fillna(0)

    # ----------------------------
    # FEATURE 1: PRICE PRESSURE
    # ----------------------------
    df["charge_per_tenure"] = df["MonthlyCharges"] / (df["tenure"] + 1)

    # ----------------------------
    # FEATURE 2: SERVICE ENGAGEMENT
    # ----------------------------
    services = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    df["num_services"] = (df[services] == "Yes").sum(axis=1)

    # ----------------------------
    # FEATURE 3: CUSTOMER LIFECYCLE
    # ----------------------------
    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 72],
        labels=["0-1yr", "1-2yr", "2-4yr", "4-6yr"],
        include_lowest=True
    )

    return df
