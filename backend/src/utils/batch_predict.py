import pandas as pd
import joblib
from src.feature.feature_engineering import feature_engineering
from src.utils.schema import REQUIRED_COLUMNS

MODEL_PATH = "src/model/churn_model.pkl"
model = joblib.load(MODEL_PATH)

# ------------------------
# Risk Bucketing
# ------------------------
def risk_bucket(prob):
    if prob < 0.3:
        return "Low Risk"
    elif prob < 0.6:
        return "Medium Risk"
    else:
        return "High Risk"

# ------------------------
# Action Recommendation
# ------------------------
def recommend_action(risk):
    if risk == "High Risk":
        return "Immediate retention offer & contract upgrade"
    elif risk == "Medium Risk":
        return "Engagement campaign & personalized discount"
    else:
        return "Upsell & loyalty rewards"

# ------------------------
# MAIN FUNCTION
# ------------------------
def run_batch_prediction(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Validate schema
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Safety conversions
    df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce").fillna(0)
    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce").fillna(0)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

    # Feature engineering
    df_fe = feature_engineering(df)

    # Prediction
    probs = model.predict_proba(df_fe)[:, 1]

    df["Churn_Probability"] = probs
    df["Risk_Level"] = df["Churn_Probability"].apply(risk_bucket)

    # Revenue risk (12 months)
    df["Revenue_At_Risk"] = df["Churn_Probability"] * df["MonthlyCharges"] * 12

    # Actions
    df["Recommended_Action"] = df["Risk_Level"].apply(recommend_action)

    return df[
        [
            "customerID",
            "Churn_Probability",
            "Risk_Level",
            "Revenue_At_Risk",
            "Recommended_Action"
        ]
    ]
