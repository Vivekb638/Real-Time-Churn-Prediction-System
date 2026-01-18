from fastapi import FastAPI, UploadFile, File
from typing import Dict
import pandas as pd
import joblib
from src.utils.preprocessing import apply_feature_engineering
from src.utils.schema import REQUIRED_COLUMNS
# ==================================================
# APP INITIALIZATION
# ==================================================
app = FastAPI(
    title="Customer Churn Decision Intelligence API",
    description="Predict churn, quantify revenue risk, and support enterprise decision-making",
    version="1.0.0"
)
MODEL_PATH = "src/model/churn_model.pkl"
model = joblib.load(MODEL_PATH)
# ==================================================
# HELPERS
# ==================================================
def risk_segment(prob: float) -> str:
    if prob < 0.4:
        return "Low Risk"
    elif prob < 0.7:
        return "Medium Risk"
    else:
        return "High Risk"
def recommend_action(risk: str) -> str:
    if risk == "High Risk":
        return "Immediate retention offer & contract upgrade"
    elif risk == "Medium Risk":
        return "Engagement campaign & personalized discount"
    else:
        return "Loyalty rewards & upsell opportunity"
# ==================================================
# HEALTH CHECK
# ==================================================
@app.get("/")
def health_check():
    return {"status": "API is running"}

# ==================================================
# SINGLE CUSTOMER PREDICTION
# ==================================================
@app.post("/predict")
def predict_single(payload: Dict):
    """
    Predict churn probability for a single customer
    """
    try:
        df = pd.DataFrame([payload])
        # Schema validation
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            return {
                "error": "Dataset missing required columns",
                "missing_columns": missing
            }

        # Ensure customerID exists for reporting
        if "customerID" not in df.columns:
            df["customerID"] = df.index.astype(str)
        # Force numeric safety
        for col in ["tenure", "MonthlyCharges", "TotalCharges"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        # Feature engineering
        df = pd.DataFrame([payload])

        # APPLY FEATURE ENGINEERING
        df = apply_feature_engineering(df)

        churn_prob = model.predict_proba(df)[0][1]

        risk = risk_segment(churn_prob)

        return {
            "churn_probability": churn_prob,
            "risk_level": risk,
            "churn_prediction": "Yes" if churn_prob >= 0.5 else "No",
            "recommended_action": recommend_action(risk)
        }

    except Exception as e:
        return {"error": str(e)}

# ==================================================
# BATCH PREDICTION (ENTERPRISE)
# ==================================================
@app.post("/predict-batch")
def predict_batch(file: UploadFile = File(...)):

    try:
        df = pd.read_csv(file.file)

        # -------------------------------
        # GUARANTEE customerID
        # -------------------------------
        if "customerID" not in df.columns:
            df.insert(0, "customerID", ["CUST_" + str(i) for i in range(1, len(df) + 1)])

        # -------------------------------
        # SCHEMA VALIDATION
        # -------------------------------
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            return {
                "error": "Dataset missing required columns",
                "missing_columns": missing
            }

        # -------------------------------
        # FEATURE ENGINEERING (NO ID)
        # -------------------------------
        df_features = apply_feature_engineering(
            df.drop(columns=["customerID"], errors="ignore")
        )

        # -------------------------------
        # PREDICTIONS
        # -------------------------------
        df["churn_probability"] = model.predict_proba(df_features)[:, 1]

        df["risk_segment"] = pd.cut(
            df["churn_probability"],
            bins=[0, 0.4, 0.7, 1.0],
            labels=["Low Risk", "Medium Risk", "High Risk"]
        )

        df["revenue_at_risk"] = df["MonthlyCharges"] * df["churn_probability"] * 6

        # -------------------------------
        # SUMMARY
        # -------------------------------
        summary = (
            df.groupby("risk_segment")
            .agg(
                customers=("customerID", "count"),
                revenue_at_risk=("revenue_at_risk", "sum")
            )
            .reset_index()
        )

        return {
            "summary": summary.to_dict(orient="records"),
            "sample_predictions": df.head(20).to_dict(orient="records")
        }

    except Exception as e:
        return {"error": str(e)}
