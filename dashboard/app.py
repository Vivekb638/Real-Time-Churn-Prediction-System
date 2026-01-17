

import streamlit as st
import requests
import base64
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Churn Decision Intelligence",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# BACKGROUND IMAGE LOADER (YOUR EXACT PATH STYLE)
# --------------------------------------------------
def load_bg_image(image_path: Path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

BASE_DIR = Path(__file__).resolve().parent.parent
BG_IMAGE = BASE_DIR / "src" / "public" / "image" / "bg.png"

bg_base64 = load_bg_image(BG_IMAGE)

# --------------------------------------------------
# GLOBAL STYLES (MAIN + SIDEBAR)
# --------------------------------------------------
st.markdown(
    f"""
    <style>
    /* MAIN BACKGROUND */
    .stApp {{
        background-image:
            linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.85)),
            url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* SIDEBAR BACKGROUND */
    section[data-testid="stSidebar"] {{
        background-image:
            linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.9)),
            url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        border-right: 1px solid rgba(255,255,255,0.08);
    }}

    section[data-testid="stSidebar"] * {{
        color: #f2f2f2 !important;
    }}

    /* HOVER CARDS */
    .section-card {{
        background: rgba(20,25,40,0.75);
        border-radius: 18px;
        padding: 26px;
        margin-bottom: 25px;
        transition: all 0.25s ease;
        border: 1px solid rgba(255,255,255,0.05);
    }}

    .section-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0px 18px 45px rgba(0,0,0,0.6);
        border: 1px solid rgba(79,172,254,0.6);
    }}

    /* BUTTONS */
    .stButton > button {{
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        color: #000;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6em 1.4em;
        border: none;
    }}

    /* METRICS */
    [data-testid="stMetric"] {{
        background: rgba(0,0,0,0.35);
        padding: 18px;
        border-radius: 14px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="section-card">
    <h1 style="text-align:center;">📊 Customer Churn Decision Intelligence System</h1>
    <p style="text-align:center; font-size:17px;">
        Predict churn, explain why customers leave, quantify revenue risk,
        and recommend data-driven retention actions.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR NAVIGATION (4 SECTIONS)
# --------------------------------------------------
st.sidebar.title("📂 Sections")

section = st.sidebar.radio(
    "Navigate",
    [
        "Customer Profile",
        "Services",
        "Billing",
        "Prediction Result"
    ]
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "payload" not in st.session_state:
    st.session_state.payload = {}

# --------------------------------------------------
# CUSTOMER PROFILE
# --------------------------------------------------
if section == "Customer Profile":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("👤 Customer Profile")

    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["Yes", "No"])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.number_input("Tenure (months)", 0, 72, 12)

    st.session_state.payload.update({
        "gender": gender,
        "SeniorCitizen": 1 if senior == "Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure
    })
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# SERVICES
# --------------------------------------------------
elif section == "Services":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📡 Services")

    phone = st.selectbox("Phone Service", ["Yes", "No"])
    multiple = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    device = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    tech = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    st.session_state.payload.update({
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": device,
        "TechSupport": tech,
        "StreamingTV": tv,
        "StreamingMovies": movies
    })
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# BILLING
# --------------------------------------------------
elif section == "Billing":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("💳 Billing")

    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly = st.number_input("Monthly Charges ($)", 0.0, 200.0, 70.0)
    total = st.number_input("Total Charges ($)", 0.0, 10000.0, 2000.0)

    st.session_state.payload.update({
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    })
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# PREDICTION RESULT
# --------------------------------------------------
elif section == "Prediction Result":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📈 Prediction Result")

    if st.button("🔍 Predict Churn Risk"):
        with st.spinner("Running Decision Intelligence Engine..."):
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=st.session_state.payload
            )

        if response.status_code != 200:
            st.error("❌ Backend API not reachable")
        else:
            result = response.json()

            if "error" in result:
                st.error(result["error"])
            else:
                churn_prob = result["churn_probability"]
                churn_label = result["churn_prediction"]

                st.metric("Churn Probability", f"{churn_prob:.2%}")

                if churn_label == "Yes":
                    st.error("High Risk of Churn")
                else:
                    st.success("Low Risk of Churn")

                st.divider()

                st.subheader("💰 Revenue Impact")
                revenue_risk = churn_prob * st.session_state.payload["MonthlyCharges"] * 6
                st.metric(
                    "Estimated Revenue at Risk (6 months)",
                    f"$ {revenue_risk:,.0f}"
                )

                st.divider()

                st.subheader("🎯 Recommended Actions")
                if churn_prob >= 0.7:
                    st.error("🚨 Immediate intervention required")
                elif churn_prob >= 0.4:
                    st.warning("⚠ Moderate risk – proactive engagement recommended")
                else:
                    st.success("✅ Low risk – maintain engagement")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div style="text-align:center; color:#aaaaaa; margin-top:40px;">
Decision Intelligence System | ML · FastAPI · Streamlit
</div>
""", unsafe_allow_html=True)

