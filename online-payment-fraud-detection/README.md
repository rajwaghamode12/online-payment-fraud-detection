# AI-Based Online Payment Fraud Detection and Risk Analysis System

## Introduction
Online payment fraud is a growing concern for businesses and consumers. This project is a machine learning-based system designed to analyze transaction data in real-time and predict whether a payment is genuine or fraudulent.

## Problem Statement
Traditional rule-based fraud detection systems are slow and often fail to detect new patterns of fraud. Automated, intelligent systems using Machine Learning are required to analyze hundreds of variables quickly and accurately to protect financial assets without blocking genuine users.

## Objectives
- To build a predictive model capable of classifying transactions as fraudulent or genuine.
- To handle class imbalance typical in financial datasets.
- To provide a risk score (0-100) and explainable reasons for suspicious transactions.
- To provide a user-friendly dashboard for checking transactions and monitoring system activity.

## Technologies
- **Python**: Core programming language.
- **Flask**: Web framework for the backend.
- **Pandas & NumPy**: Data manipulation and numerical operations.
- **Scikit-learn & Imbalanced-learn**: Machine learning model building and SMOTE.
- **SQLite**: Lightweight database for storing users and transactions.
- **HTML/CSS/JavaScript/Bootstrap**: Frontend user interface.
- **Chart.js**: Data visualization in the admin dashboard.

## Workflow
1. User creates an account and logs in.
2. User enters transaction details into the form.
3. The Flask backend receives the data and passes it to a preprocessor to encode and scale it.
4. The preprocessed data is fed into a trained Random Forest model.
5. The model outputs a probability of fraud, which is converted to a Risk Score (Low, Medium, High).
6. The system explains the prediction (e.g., "Unusual transaction amount") and records it in the database.
7. The Admin can view the overall statistics and model performance.

## Machine Learning
- **Random Forest**: Used as the primary model due to its high accuracy and ability to handle non-linear data without overfitting.
- **Class Imbalance**: Addressed using SMOTE (Synthetic Minority Over-sampling Technique) to ensure the model learns to identify fraud correctly rather than just guessing "Genuine" every time.
- **Evaluation**: The model is evaluated based on Accuracy, Precision, Recall, and F1-score, with a special emphasis on Recall (catching as many frauds as possible).

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Generate the dataset and train the model:
   ```bash
   python dataset/generate_data.py
   python model/train_model.py
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and go to `http://127.0.0.1:5000`

### Demo Accounts
- **Admin**: Email `admin@demo.com` | Password `admin123`
- You can create your own standard user account by clicking "Register".
