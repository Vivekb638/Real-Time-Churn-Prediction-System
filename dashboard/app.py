import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


import streamlit as st
import requests
import pandas as pd
# import os
from dotenv import load_dotenv
from src.utils.pdf_report import generate_churn_pdf
import tempfile

# =========================================================
# LOAD ENV
# =========================================================
load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ChurnAI | Decision Intelligence",
    page_icon="🔮",
    layout="wide",
)

# =========================================================
# STYLING
# =========================================================
def apply_custom_design():
    bg_img_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072"
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(14,17,23,0.85), rgba(14,17,23,0.85)),
                    url("{bg_img_url}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .glass {{
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(14px);
        border-radius: 18px;
        padding: 30px;
        border: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 25px;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_custom_design()

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<h1 style="text-align:center;">🚀 CHURN<span style="color:#3b82f6;">.AI</span></h1>
<p style="text-align:center;opacity:0.8;">
Predict churn · Quantify revenue risk · Recommend actions
</p>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    mode = st.radio("Select Mode", ["Individual Customer", "Enterprise"])
    st.divider()
    st.success("Model: Logistic Regression")
    st.caption("Decision Intelligence Enabled")

# =========================================================
# INDIVIDUAL MODE
# =========================================================
if mode == "Individual Customer":

    tab1, tab2, tab3 = st.tabs(["👤 Profile", "📡 Services", "💳 Billing"])

    with tab1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        gender = c1.selectbox("Gender", ["Male", "Female"])
        senior = c1.selectbox("Senior Citizen", ["No", "Yes"])
        partner = c2.selectbox("Partner", ["No", "Yes"])
        dependents = c2.selectbox("Dependents", ["No", "Yes"])
        tenure = c3.number_input("Tenure (Months)", 0, 72, 12)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        tech = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        streaming = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        monthly = st.number_input("Monthly Charges ($)", 0.0, 200.0, 70.0)
        payment = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer", "Credit card"]
        )
        total = st.number_input("Total Charges ($)", 0.0, 10000.0, 2000.0)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 RUN INTELLIGENCE ENGINE", use_container_width=True):

        payload = {
            "gender": gender,
            "SeniorCitizen": 1 if senior == "Yes" else 0,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "InternetService": internet,
            "OnlineSecurity": security,
            "TechSupport": tech,
            "StreamingTV": streaming,
            "Contract": contract,
            "MonthlyCharges": monthly,
            "PaymentMethod": payment,
            "TotalCharges": total,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "StreamingMovies": "No",
            "PaperlessBilling": "Yes"
        }

        with st.spinner("🧠 Predicting churn..."):
            response = requests.post(f"{API_URL}/predict", json=payload)
            result = response.json()

        # ✅ SAFE HANDLING (FIXES YOUR ERROR)
        if "error" in result:
            st.error(result["error"])
            st.stop()

        prob = result.get("churn_probability")
        if prob is None:
            st.error("Invalid API response")
            st.json(result)
            st.stop()

        revenue_risk = prob * monthly * 12

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Churn Probability", f"{prob:.1%}")
        c3.metric("Annual Revenue Risk", f"${revenue_risk:,.0f}")

        if prob >= 0.7:
            c2.error("🔴 HIGH RISK")
        elif prob >= 0.4:
            c2.warning("🟠 MEDIUM RISK")
        else:
            c2.success("🟢 LOW RISK")

        st.subheader("🎯 Recommended Action")
        if prob >= 0.7:
            st.error("Immediate retention offer + contract upgrade")
        elif prob >= 0.4:
            st.warning("Engagement campaign + loyalty incentives")
        else:
            st.success("Maintain relationship, upsell opportunity")

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ENTERPRISE MODE
# =========================================================
# =========================================================
# ENTERPRISE MODE (BATCH DECISION INTELLIGENCE)
# =========================================================
# =========================================================
# ENTERPRISE MODE — DASHBOARD
# =========================================================
else:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("🏢 Enterprise Decision Intelligence")

    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 Company Details",
        "📤 Upload Dataset",
        "📊 Dashboard",
        "📄 PDF Report"
    ])

    # =====================================================
    # TAB 1 — COMPANY DETAILS
    # =====================================================
    with tab1:
        st.markdown("### Company Information")
        c1, c2 = st.columns(2)

        with c1:
            company_name = st.text_input("Company Name")
            company_email = st.text_input("Company Email")

        with c2:
            company_location = st.text_input("Location")
            company_website = st.text_input("Website")

        st.info("ℹ️ This information will be included in the executive PDF report.")

    # =====================================================
    # TAB 2 — DATASET UPLOAD + BATCH PREDICTION
    # =====================================================
    with tab2:
        st.subheader("📋 Required Dataset Schema")

        schema_df = pd.DataFrame({
            "Order": range(1, 21),
            "Column Name": [
                "customerID","gender","SeniorCitizen","Partner","Dependents","tenure",
                "PhoneService","MultipleLines","InternetService","OnlineSecurity",
                "OnlineBackup","DeviceProtection","TechSupport","StreamingTV",
                "StreamingMovies","Contract","PaperlessBilling","PaymentMethod",
                "MonthlyCharges","TotalCharges"
            ],
            "Type": [
                "String","Category","Integer","Category","Category","Integer",
                "Category","Category","Category","Category",
                "Category","Category","Category","Category",
                "Category","Category","Category","Category",
                "Float","Float"
            ]
        })

        st.dataframe(schema_df, use_container_width=True)

        st.info(
            "📌 **Important:**\n"
            "- Column names must match exactly\n"
            "- Order should be the same\n"
            "- Accepted file formats: CSV or Excel\n"
        )

        sample_csv = """customerID,gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges
        CUST_001,Male,0,Yes,No,12,Yes,No,DSL,Yes,Yes,No,Yes,No,No,One year,Yes,Credit card,75.5,906.0
        """

        st.download_button(
            label="⬇ Download Sample Dataset",
            data=sample_csv,
            file_name="sample_enterprise_dataset.csv",
            mime="text/csv"
        )


        st.markdown("### Upload Customer Dataset")

        uploaded = st.file_uploader(
            "Upload CSV or Excel file",
            type=["csv", "xlsx"]
        )

        if uploaded:
            try:
                file_bytes = uploaded.read()

                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(pd.io.common.BytesIO(file_bytes))
                else:
                    df = pd.read_excel(pd.io.common.BytesIO(file_bytes))

                st.success("✅ Dataset uploaded successfully")
                st.dataframe(df.head(), use_container_width=True)

                st.session_state["uploaded_file"] = file_bytes
                st.session_state["uploaded_file_name"] = uploaded.name

            except Exception as e:
                st.error(f"❌ File read error: {e}")
                st.stop()

        if st.button("🚀 Run Batch Prediction"):
            if "uploaded_file" not in st.session_state:
                st.error("Please upload a dataset first")
                st.stop()

            files = {
                "file": (
                    st.session_state["uploaded_file_name"],
                    st.session_state["uploaded_file"],
                    "application/octet-stream"
                )
            }

            with st.spinner("Running enterprise churn analysis..."):
                response = requests.post(
                    f"{API_URL}/predict-batch",
                    files=files,
                    timeout=120
                )

            result = response.json()

            if "error" in result:
                st.error(result["error"])
                st.stop()

            st.success("✅ Batch prediction completed")

            st.session_state["batch_summary"] = pd.DataFrame(result["summary"])
            st.session_state["batch_samples"] = pd.DataFrame(result["sample_predictions"])

    # =====================================================
    # TAB 3 — ENTERPRISE DASHBOARD
    # =====================================================
    with tab3:
        if "batch_summary" not in st.session_state:
            st.warning("⚠️ Run batch prediction first")
            st.stop()

        summary_df = st.session_state["batch_summary"]
        samples_df = st.session_state["batch_samples"]

        # -------------------------------
        # COMPANY OVERVIEW
        # -------------------------------
        st.markdown("## 🏢 Company Overview")

        c1, c2, c3 = st.columns(3)
        c1.metric("Company", company_name or "—")
        c2.metric("Location", company_location or "—")
        c3.metric("Total Customers", samples_df.shape[0])

        st.divider()

        # -------------------------------
        # RISK SEGMENTATION
        # -------------------------------
        st.markdown("## 📊 Portfolio Risk Distribution")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Customer Count by Risk")
            st.bar_chart(
                summary_df.set_index("risk_segment")["customers"]
            )

        with col2:
            st.subheader("Revenue at Risk")
            st.bar_chart(
                summary_df.set_index("risk_segment")["revenue_at_risk"]
            )

        st.divider()

        # -------------------------------
        # FEATURE VS CHURN ANALYSIS
        # -------------------------------
        st.markdown("## 🔍 Feature Impact on Churn")

        samples_df["PredictedChurn"] = samples_df["risk_segment"]

        def feature_churn_chart(feature):
            chart_df = pd.crosstab(samples_df[feature], samples_df["PredictedChurn"])
            st.subheader(f"{feature} vs Churn")
            st.bar_chart(chart_df)

        feature_churn_chart("gender")
        feature_churn_chart("Partner")
        feature_churn_chart("Contract")
        feature_churn_chart("InternetService")

        st.divider()

        st.markdown("## 🧪 Sample Predictions")
        st.dataframe(samples_df.head(25), use_container_width=True)

    # =====================================================
    # TAB 4 — PDF REPORT
    # =====================================================
    with tab4:
        if "batch_summary" not in st.session_state:
            st.warning("⚠️ Run batch prediction first")
            st.stop()

        if st.button("📄 Generate Executive PDF"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                generate_churn_pdf(
                    company_info={
                        "name": company_name,
                        "location": company_location,
                        "email": company_email,
                        "website": company_website
                    },
                    summary_df=st.session_state["batch_summary"],
                    output_path=tmp.name
                )

                with open(tmp.name, "rb") as f:
                    st.download_button(
                        label="⬇ Download PDF Report",
                        data=f,
                        file_name="Churn_Decision_Intelligence_Report.pdf",
                        mime="application/pdf"
                    )

    st.markdown('</div>', unsafe_allow_html=True)



# =========================================================
# FOOTER
# =========================================================
st.caption("ChurnAI · Decision Intelligence Platform · ML + FastAPI + Streamlit")

