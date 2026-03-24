# 🚀 Real-Time Churn Prediction System  
### Decision Intelligence Platform for Customer Retention

🔗 **Live Application (Frontend):**  
👉 (https://real-time-churn-prediction-system-k.vercel.app/)

---

## 📌 Overview

The **Real-Time Churn Prediction System** is a full-stack **Machine Learning–powered decision intelligence platform** designed to help businesses:

- Predict customer churn in real time  
- Quantify potential revenue loss  
- Take proactive, data-driven retention actions  

This project transforms a churn prediction model into a **production-ready enterprise solution** with:

- Real-time individual predictions  
- Enterprise-scale batch analysis  
- Interactive dashboards  
- Executive-level PDF reports  

---

## 🧠 Key Capabilities

### 👤 Individual Customer Analysis
- Real-time churn probability prediction  
- Risk classification:
  - 🟢 **Low Risk**
  - 🟠 **Medium Risk**
  - 🔴 **High Risk**
- Annual revenue loss estimation  
- Actionable business recommendations  

---

### 🏢 Enterprise Decision Intelligence

A complete **4-step enterprise workflow**:

#### 1️⃣ Company Details
- Company name  
- Location  
- Email address  
- Website  

#### 2️⃣ Dataset Upload
- Upload customer data (**CSV / Excel**)  
- Automatic schema validation  
- Intelligent customer ID handling  

#### 3️⃣ Enterprise Dashboard
- Risk segmentation distribution  
- Revenue-at-risk analysis  
- Feature vs churn insights:
  - Gender vs Churn  
  - Contract vs Churn  
  - Partner vs Churn  
  - Internet Service vs Churn  

#### 4️⃣ Executive PDF Report
- Company overview  
- Risk summary  
- Revenue impact analysis  
- Customer-level decision table:
  - Customer ID  
  - Churn probability  
  - Risk level  
  - Annual revenue loss  
  - Recommended action  

---

## 🏗️ System Architecture

User (Browser)
│
▼
Frontend (React + Vite + TailwindCSS)
│ REST API Calls (JSON)
▼
Backend (FastAPI)
│ ML Inference & Rule Logic
▼
Churn Prediction Output & PDF Engine


---

## 🧩 Technology Stack

### 🔹 Core Intelligence & Data
- **Machine Learning**: Scikit-Learn (Logistic Regression, Random Forest, etc.)
- **Data Engineering**: Pandas, NumPy
- **Analysis**: Matplotlib, Seaborn

### 🔹 Backend API
- **Framework**: FastAPI (Async)
- **Server**: Uvicorn
- **Serialization**: Joblib
- **Reporting**: ReportLab (Dynamic PDF Engine)

### 🔹 Frontend Client
- **Framework**: React.js (Vite)
- **Styling**: TailwindCSS v4 (Glassmorphism UI)
- **Routing**: React Router DOM
- **Visualization**: Recharts (Pie/Bar/Metrics)
- **Icons**: Lucide-React

---

## 📁 Project Structure (Monorepo)

Real-Time-Churn-Prediction-System/
│
├── frontend/                 # React SPA Client
│   ├── src/
│   │   ├── components/       # UI Elements
│   │   ├── pages/            # Views (Dashboard, Individual)
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                  # FastAPI & ML Engine
│   ├── src/
│   │   ├── api/              # Endpoints (main.py)
│   │   ├── utils/            # Preprocessing, schema, PDF logic
│   │   ├── train_models.py   # Automated 10-model trainer
│   │   └── model/            # Serialized models
│   ├── data/                 # Raw/Sample datasets
│   └── requirements.txt
│
├── analysis.md               # Business Intelligence & Findings
├── README.md
└── .gitignore

---

## ⚙️ Installation & Local Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vivekb638/Real-Time-Churn-Prediction-System.git
cd Real-Time-Churn-Prediction-System
```

### 2️⃣ Start the Intelligence Backend (FastAPI)
Open a terminal and navigate to the backend folder:
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

# Install ML & API dependencies
pip install -r requirements.txt

# Launch Server
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```
*The API will be operational at: 👉 http://127.0.0.1:8000*

### 3️⃣ Start the Frontend Client (React)
Open a new terminal and navigate to the frontend folder:
```bash
cd frontend

# Install Node modules
npm install

# Launch Development Server
npm run dev
```
*The Dashboard will open at: 👉 http://localhost:5173*

---

## 📊 Business Impact
- **Early Identification**: Predict churn risk in real-time.
- **Revenue Quantification**: Calculate exact annual revenue at risk.
- **Actionable AI Strategies**: Dynamically generates targeted 1-of-11 retention actions based on the specific customer profile.
- **Executive Reporting**: One-click categorized enterprise PDF exports.

---

## 👨‍💻 Author
**Vineet Baghel**  
*Machine Learning & Data Science Enthusiast*

This project demonstrates a complete end-to-end ML engineering pipeline: Model Training -> Backend Service -> Dynamic React Dashboard -> Policy Generation.

⭐ If you find this project useful, please consider giving it a star on GitHub! ⭐

