import pandas as pd

def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ---------------------------
    # DEFAULT VALUES (CRITICAL)
    # ---------------------------
    defaults = {
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "StreamingMovies": "No",
        "PaperlessBilling": "Yes"
    }

    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val

    # Safety casting
    df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce").fillna(0)
    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce").fillna(0)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

    # Feature engineering
    df["charge_per_tenure"] = df["MonthlyCharges"] / (df["tenure"] + 1)

    services = [
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    df["num_services"] = (df[services] == "Yes").sum(axis=1)

    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 72],
        labels=["0-1yr", "1-2yr", "2-4yr", "4-6yr"],
        include_lowest=True
    )

    return df
