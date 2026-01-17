from fastapi import FastAPI, UploadFile, File
import pandas as pd
import joblib
import os
import sys

# -----------------------------
# PATH FIX
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.feature.feature_engineering import feature_engineering

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI(
    title="Customer Churn Decision Intelligence API",
    version="1.0"
)

# -----------------------------
# LOAD MODEL
# -----------------------------
MODEL_PATH = os.path.join(BASE_DIR, "src", "model", "churn_model.pkl")
model = joblib.load(MODEL_PATH)

# -----------------------------
# HEALTH
# -----------------------------
@app.get("/")
def health():
    return {"status": "running"}

# -----------------------------
# SINGLE PREDICTION
# -----------------------------
@app.post("/predict")
def predict(data: dict):
    try:
        df = pd.DataFrame([data])
        df = feature_engineering(df)

        prob = model.predict_proba(df)[0][1]
        pred = "Yes" if prob >= 0.5 else "No"

        return {
            "churn_probability": float(prob),
            "churn_prediction": pred
        }

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# BATCH PREDICTION
# -----------------------------
@app.post("/predict-batch")
def predict_batch(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        customer_ids = df.get("customerID", df.index.astype(str))
        df = df.drop(columns=["customerID"], errors="ignore")

        df = feature_engineering(df)

        probs = model.predict_proba(df)[:, 1]

        result = pd.DataFrame({
            "customerID": customer_ids,
            "churn_probability": probs,
            "risk_category": pd.cut(
                probs,
                bins=[0, 0.4, 0.7, 1.0],
                labels=["Low", "Medium", "High"]
            )
        })

        return {
            "summary": result["risk_category"].value_counts().to_dict(),
            "records": result.to_dict(orient="records")
        }

    except Exception as e:
        return {"error": str(e)}
