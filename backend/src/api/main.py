from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import pandas as pd
import joblib
import tempfile
import os
from src.utils.preprocessing import apply_feature_engineering
from src.utils.schema import REQUIRED_COLUMNS
from src.utils.pdf_report import generate_churn_pdf

# ==================================================
# APP INITIALIZATION
# ==================================================
app = FastAPI(
    title="Customer Churn Decision Intelligence API",
    description="Predict churn, quantify revenue risk, and support enterprise decision-making",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
def generate_retention_strategy(payload: dict, churn_prob: float) -> str:
    tenure = float(payload.get('tenure', 0))
    monthly_charges = float(payload.get('MonthlyCharges', 0))
    contract = payload.get('Contract', 'Month-to-month')
    tech_support = payload.get('TechSupport', 'No')
    payment_method = payload.get('PaymentMethod', 'Electronic check')
    
    if churn_prob > 0.7:  # High Risk
        if monthly_charges > 80:
            return "VIP Intervention Required: Premium customer at critical churn risk. Assign a dedicated retention specialist to call immediately. Offer a customized 20% loyalty discount or a complimentary service upgrade for 6 months."
        elif tenure < 6:
            return "Early-Stage Rescue: Customer is highly likely to churn early, indicating poor onboarding. Deploy an automated 'We Miss You' campaign offering a 1-month free credit and schedule a proactive technical check-in."
        elif contract == 'Month-to-month':
            return "Contract Lock-In Motivation: High volatility due to lack of commitment. Send a targeted email offering an exclusive 'Price Lock Guarantee' and free device protection if they upgrade to a 1-year contract today."
        else:
            return "Urgent Account Review: Dispatch an immediate personalized email from the account manager with a survey to identify dissatisfaction points, accompanied by a $25 no-strings-attached account credit."
            
    elif churn_prob > 0.4:  # Medium Risk
        if tech_support == 'No':
            return "Service Confidence Boost: Customer shows distress and lacks technical support. Proactively grant complimentary priority Tech Support for 3 months and email a 'Top Ways to Optimize Your Connection' guide."
        elif tenure > 24:
            return "Loyalty Appreciation: Veteran customer experiencing mid-tier risk. Avoid discounts; instead, send a personalized 'Thank You' package acknowledging their loyalty alongside a free speed upgrade as a token of appreciation."
        elif payment_method in ['Electronic check', 'Mailed check']:
            return "Payment Friction Reduction: Manual payment methods often cause accidental churn. Trigger a campaign offering a $10 one-time credit if they switch their payment method to Auto-Pay via Credit Card."
        else:
            return "Engagement Nudge: Monitor usage patterns over 30 days. Send a targeted 'Did you know?' newsletter highlighting underutilized features of their current plan to increase daily platform reliance."
            
    else:  # Low Risk
        if monthly_charges < 50:
            return "Growth & Upsell Opportunity: Highly stable customer on a low-tier plan. Add them to the targeted marketing cadence for premium packages, highlighting the benefits of Fiber Optic internet at a marginal price increase."
        elif tenure > 12 and monthly_charges > 70:
            return "Advocacy Activation: Highly satisfied premium customer. Leverage their satisfaction by inviting them to an exclusive Customer Advisory Board or sending a Referral Code to earn $50 for every friend they bring."
        else:
            return "Maintain Satisfaction: No immediate retention intervention needed. Continue delivering excellent service and include them in general seasonal promotional communications to maintain brand positivity."
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
            "recommended_action": generate_retention_strategy(payload, churn_prob)
        }

    except Exception as e:
        return {"error": str(e)}

# ==================================================
# BATCH PREDICTION (ENTERPRISE)
# ==================================================
@app.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):

    try:
        import io
        contents = await file.read()
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        # -------------------------------
        # GUARANTEE customerID & customerName
        # -------------------------------
        df.columns = df.columns.str.strip()
        
        if "customerID" not in df.columns:
            df.insert(0, "customerID", ["CUST_" + str(i) for i in range(1, len(df) + 1)])
        if "customerName" not in df.columns:
            df.insert(1, "customerName", ["Unknown" for i in range(len(df))])

        # -------------------------------
        # SCHEMA VALIDATION
        # -------------------------------
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            return {
                "error": f"Dataset missing required columns: {', '.join(missing)}",
                "missing_columns": missing
            }

        # -------------------------------
        # FEATURE ENGINEERING (NO ID)
        # -------------------------------
        df_features = apply_feature_engineering(
            df.drop(columns=["customerID", "customerName"], errors="ignore")
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

        all_preds = df[["customerID", "customerName", "risk_segment", "churn_probability", "revenue_at_risk"]].to_dict(orient="records")

        return {
            "summary": summary.to_dict(orient="records"),
            "sample_predictions": df.head(20).to_dict(orient="records"),
            "all_predictions": all_preds
        }

    except Exception as e:
        return {"error": str(e)}

# ==================================================
# GENERATE PDF REPORT
# ==================================================
from pydantic import BaseModel

class ReportRequest(BaseModel):
    company_name: str = ""
    company_location: str = ""
    company_email: str = ""
    company_website: str = ""
    summary_data: List[Dict[str, Any]]
    customer_lists: Dict[str, List[Dict[str, Any]]] = {}

def remove_file(path: str):
    try:
        os.unlink(path)
    except Exception:
        pass

@app.post("/generate-report")
def generate_report(payload: ReportRequest, background_tasks: BackgroundTasks):
    try:
        company_info = {
            "name": payload.company_name,
            "location": payload.company_location,
            "email": payload.company_email,
            "website": payload.company_website
        }
        
        summary_df = pd.DataFrame(payload.summary_data)
        
        # Create temp file for PDF
        fd, temp_pdf_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)
        
        generate_churn_pdf(
            company_info=company_info,
            summary_df=summary_df,
            customer_lists=payload.customer_lists,
            output_path=temp_pdf_path
        )
        
        # Delete the temp file after returning
        background_tasks.add_task(remove_file, temp_pdf_path)
        
        return FileResponse(
            temp_pdf_path, 
            media_type="application/pdf", 
            filename="Churn_Decision_Intelligence_Report.pdf"
        )
    except Exception as e:
        return {"error": str(e)}
