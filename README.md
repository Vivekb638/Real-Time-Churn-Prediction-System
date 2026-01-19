# 🚀 Real-Time Churn Prediction System  
### Decision Intelligence Platform for Customer Retention

🔗 **Live Application (Frontend):**  
👉 https://real-time-churn-prediction-system.streamlit.app/

---

## 📌 Overview

The **Real-Time Churn Prediction System** is a full-stack Machine Learning application designed to help businesses **predict customer churn**, **quantify revenue loss**, and **take proactive retention actions**.

This project converts a churn prediction ML model into a **production-ready decision intelligence platform** with:
- Real-time individual predictions
- Enterprise batch analysis
- Interactive dashboards
- Executive-level PDF reports

---

## 🧠 Key Capabilities

### 👤 Individual Customer Analysis
- Predicts churn probability in real time
- Classifies customers into:
  - 🟢 Low Risk  
  - 🟠 Medium Risk  
  - 🔴 High Risk
- Estimates annual revenue loss
- Provides actionable business recommendations

---

### 🏢 Enterprise Decision Intelligence
A complete 4-step enterprise workflow:

1. **Company Details**
   - Company name
   - Location
   - Email
   - Website

2. **Dataset Upload**
   - Upload customer data (CSV / Excel)
   - Automatic schema validation
   - Customer ID handling

3. **Enterprise Dashboard**
   - Risk segmentation distribution
   - Revenue-at-risk analysis
   - Feature vs churn analysis:
     - Gender vs churn
     - Contract vs churn
     - Partner vs churn
     - Internet service vs churn

4. **Executive PDF Report**
   - Company overview
   - Risk summary
   - Revenue impact
   - Customer-level decision table:
     - Customer ID
     - Churn probability
     - Risk level
     - Annual revenue loss
     - Recommended action

---

## 🏗️ System Architecture

User (Browser)
|
| Streamlit UI
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


---

## 🧩 Technology Stack

### Machine Learning
- Scikit-learn
- Logistic Regression
- Feature Engineering
- Probability-based segmentation

### Backend
- FastAPI
- Uvicorn
- Joblib

### Frontend
- Streamlit
- Interactive dashboards

### Data & Visualization
- Pandas
- NumPy
- Matplotlib
- Seaborn

### Reporting
- ReportLab (PDF generation)

---

## 📁 Project Structure

Real-Time-Churn-Prediction-System/
│
├── dashboard/
│ └── app.py # Streamlit frontend
│
├── src/
│ ├── api/
│ │ └── main.py # FastAPI backend
│ ├── model/
│ │ └── churn_model.pkl
│ └── utils/
│ ├── preprocessing.py
│ ├── schema.py
│ └── pdf_report.py
│
├── requirements.txt
├── README.md
└── .env


---

## ⚙️ Installation & Setup (Run Locally)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vivekb638/Real-Time-Churn-Prediction-System.git
cd Real-Time-Churn-Prediction-System
### 2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt

## 📦 Required Dependencies

The project requires the following libraries:

**pandas
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
python-multipart**

## ▶️ Running the Project Locally
### 🔹 Start Backend (FastAPI)
uvicorn src.api.main:app --host 127.0.0.1 --port 8000


Backend will be available at:

http://127.0.0.1:8000

### 🔹 Start Frontend (Streamlit)
streamlit run dashboard/app.py


Frontend will open at:

http://localhost:8501

## 🌐 Deployment
✅ Frontend (Streamlit Cloud)

### **Live application:**
👉 https://real-time-churn-prediction-system.streamlit.app/


## 📊 Business Impact

Early identification of churn risk

Quantified revenue loss estimation

Actionable retention strategies

Enterprise-scale decision making

Executive-ready reporting

## 🔮 Future Enhancements

Model explainability (SHAP)

Authentication & role-based access

Advanced retention simulations

Cloud storage for reports

Multiple model comparison

## 👨‍💻 Author

**Vineet Baghel**
Machine Learning & Data Science Enthusiast

This project demonstrates end-to-end ML engineering, including:

Model development

Backend API design

Frontend dashboards

Enterprise reporting

Cloud deployment

## ⭐ If you find this project useful, please consider giving it a star on GitHub!
