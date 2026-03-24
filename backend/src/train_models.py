import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

# 10 Models
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, 
    AdaBoostClassifier, ExtraTreesClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

import sys
import os

# Add root to python path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils.preprocessing import apply_feature_engineering
from src.utils.schema import REQUIRED_COLUMNS

def train_and_evaluate():
    print("Loading data...")
    df = pd.read_csv("data/raw/Dataset.csv")
    
    print("Applying Feature Engineering...")
    # Drop target variable for preprocessing if it exists
    y = df['Churn'].map({'Yes': 1, 'No': 0})
    X = df.drop(columns=['Churn', 'customerID'], errors='ignore')
    
    # Fill defaults and numeric features
    X = apply_feature_engineering(X)
    
    # Categorical and numerical columns
    num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "charge_per_tenure", "num_services"]
    cat_cols = [col for col in X.columns if col not in num_cols]
    
    print(f"Num Cols: {num_cols}")
    print(f"Cat Cols: {cat_cols}")
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
        ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "AdaBoost": AdaBoostClassifier(random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Extra Trees": ExtraTreesClassifier(random_state=42),
        "MLP Classifier": MLPClassifier(max_iter=1000, random_state=42),
        "Ridge Classifier": RidgeClassifier(),
        "SVM (Linear)": SVC(kernel='linear', probability=True, random_state=42)
    }

    best_model = None
    best_score = 0
    best_name = ""
    best_pipeline = None

    print("\nTraining and evaluating 10 models...")
    for name, model in models.items():
        print(f"-> Training {name}...")
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        
        try:
            pipeline.fit(X_train, y_train)
            
            # Predict
            if name == "Ridge Classifier":
                # Ridge doesn't support predict_proba, we handle it if needed
                y_pred = pipeline.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
            else:
                y_pred = pipeline.predict(X_test)
                if hasattr(model, "predict_proba"):
                    y_prob = pipeline.predict_proba(X_test)[:, 1]
                    auc = roc_auc_score(y_test, y_prob)
                acc = accuracy_score(y_test, y_pred)
            
            print(f"   Accuracy: {acc:.4f}")
            
            if acc > best_score:
                if name != "Ridge Classifier":  # we need predict_proba in the API
                    best_score = acc
                    best_model = model
                    best_name = name
                    best_pipeline = pipeline
                    
        except Exception as e:
            print(f"   Error training {name}: {e}")
            
    print(f"\n=============================================")
    print(f"🏆 Best Model: {best_name} (Accuracy: {best_score:.4f})")
    print(f"=============================================")
    
    model_path = "src/model/churn_model.pkl"
    joblib.dump(best_pipeline, model_path)
    print(f"Saved best model pipeline to {model_path}!")

if __name__ == "__main__":
    train_and_evaluate()
