import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

def train_and_save_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'dataset', 'payment_fraud.csv')
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return
        
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    # Preprocessing
    X = df.drop('Fraud', axis=1)
    y = df['Fraud']
    
    categorical_cols = ['transaction_type', 'location', 'device_type']
    numerical_cols = ['amount', 'transaction_time', 'sender_balance', 'receiver_balance', 
                      'previous_transactions', 'new_device', 'unusual_location']
                      
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # We will save the preprocessor to use independently during prediction
    print("Fitting preprocessor...")
    X_train_preprocessed = preprocessor.fit_transform(X_train)
    X_test_preprocessed = preprocessor.transform(X_test)
    
    # Save preprocessor
    preprocessor_path = os.path.join(base_dir, 'model', 'preprocessor.pkl')
    joblib.dump(preprocessor, preprocessor_path)
    print(f"Preprocessor saved to {preprocessor_path}")
    
    # Handle class imbalance using SMOTE
    print("Applying SMOTE...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_preprocessed, y_train)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    }
    
    results = {}
    best_f1 = 0
    best_model = None
    
    print("Training models...")
    for name, model in models.items():
        model.fit(X_train_resampled, y_train_resampled)
        y_pred = model.predict(X_test_preprocessed)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        results[name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'confusion_matrix': cm.tolist()
        }
        
        print(f"\n{name} Results:")
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        
        # We always want Random Forest to be our final model, but just checking performance
        if name == 'Random Forest':
            best_model = model
            
    # Save best model
    model_path = os.path.join(base_dir, 'model', 'fraud_model.pkl')
    joblib.dump(best_model, model_path)
    print(f"\nRandom Forest Model saved to {model_path}")
    
    # Save results to a json for the admin dashboard
    import json
    results_path = os.path.join(base_dir, 'model', 'model_performance.json')
    with open(results_path, 'w') as f:
        json.dump(results, f)
    print("Model performance metrics saved.")

if __name__ == '__main__':
    train_and_save_model()
