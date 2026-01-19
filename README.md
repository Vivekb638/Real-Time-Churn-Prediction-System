🚀 Real-Time Churn Prediction System

Decision Intelligence Platform for Customer Retention

A full-stack Machine Learning + FastAPI + Streamlit application that predicts customer churn in real time, quantifies revenue risk, and provides actionable business insights for both individual customers and enterprise portfolios.

🧠 Project Overview

Customer churn is one of the biggest revenue threats for subscription-based businesses.
This project transforms a churn prediction model into a production-ready decision intelligence system.

What this system does:

Predicts churn probability for individual customers

Segments customers into Low / Medium / High Risk

Estimates revenue at risk

Provides business recommendations

Supports enterprise batch analysis

Generates executive PDF reports

Fully deployable with FastAPI backend + Streamlit frontend

🏗️ System Architecture
User (Browser)
   |
   |  Streamlit UI
   v
Frontend (Streamlit)
   |
   | REST API Calls
   v
Backend (FastAPI)
   |
   | ML Inference
   v
Churn Prediction Model (Scikit-learn)

🧩 Tech Stack
🔹 Machine Learning

Logistic Regression (Scikit-learn)

Feature Engineering

Probability-based risk segmentation

🔹 Backend

FastAPI

Uvicorn

Joblib (model loading)

🔹 Frontend

Streamlit

Interactive dashboards

Enterprise batch workflows

🔹 Data & Visualization

Pandas, NumPy

Matplotlib, Seaborn

🔹 Reporting

ReportLab (PDF generation)

🔹 Deployment

Backend: Render

Frontend: Streamlit Cloud

✨ Key Features
👤 Individual Customer Analysis

Real-time churn probability

Risk classification (Low / Medium / High)

Annual revenue loss estimation

Business action recommendations

🏢 Enterprise Decision Intelligence

4-Step Workflow

1️⃣ Company Details

Company name, location, email, website

2️⃣ Dataset Upload

CSV / Excel customer data

Schema validation

Automatic customer ID handling

3️⃣ Enterprise Dashboard

Portfolio risk distribution

Revenue-at-risk analysis

Feature vs churn analysis:

Gender vs churn

Contract vs churn

Partner vs churn

Internet service vs churn

4️⃣ Executive PDF Report

Company overview

Risk segmentation summary

Revenue impact

Customer-level decision table

📊 Example Business Outputs

Churn Probability: 72%

Risk Level: High Risk

Estimated Annual Revenue Loss: $1,240

Recommendation: Immediate retention offer & contract upgrade

📁 Project Structure
Real-Time-Churn-Prediction-System/
│
├── dashboard/
│   └── app.py              # Streamlit frontend
│
├── src/
│   ├── api/
│   │   └── main.py         # FastAPI backend
│   ├── model/
│   │   └── churn_model.pkl
│   └── utils/
│       ├── preprocessing.py
│       ├── schema.py
│       └── pdf_report.py
│
├── requirements.txt
├── README.md
└── .env

🧪 API Endpoints
Health Check
GET /

Single Customer Prediction
POST /predict

Enterprise Batch Prediction
POST /predict-batch

🚀 Deployment
Backend (FastAPI – Render)
uvicorn src.api.main:app --host 0.0.0.0 --port 10000

Frontend (Streamlit Cloud)
streamlit run dashboard/app.py

📦 Requirements
pandas
numpy
scikit-learn
matplotlib
seaborn
fastapi
uvicorn
streamlit
reportlab
python-dotenv
joblib
python-multipart

🎯 Business Value

Reduces customer churn proactively

Enables data-driven retention strategies

Quantifies financial risk

Executive-ready reporting

Scalable for enterprise use

🔮 Future Enhancements

Authentication & role-based access

Model explainability (SHAP)

A/B testing for retention strategies

Cloud storage for reports

Multi-model comparison

👨‍💻 Author

Vivek
Machine Learning & Data Science Enthusiast

📌 This project demonstrates end-to-end ML engineering, backend APIs, frontend dashboards, and production deployment.

⭐ If you like this project

Give it a ⭐ on GitHub — it really helps!
