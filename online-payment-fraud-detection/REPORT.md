# College Project Report

## 1. Title
AI-Based Online Payment Fraud Detection and Risk Analysis System

## 2. Abstract
With the rapid increase in digital transactions, online payment fraud has become a significant threat to financial institutions and customers. Traditional rule-based systems are inadequate in catching dynamic fraud patterns. This project proposes an intelligent, Machine Learning-based system designed to analyze transaction parameters in real-time and accurately classify them as genuine or fraudulent. Built using Python, Scikit-Learn, and Flask, the system provides a comprehensive dashboard for users to check transactions and for administrators to monitor network security.

## 3. Introduction
Online payment systems offer immense convenience but introduce security vulnerabilities. This project simulates a banking security layer that intercepts transactions, extracts features (such as amount, location, time, and device history), and uses a trained Random Forest model to assign a Risk Score. Transactions are then categorized into Low, Medium, or High Risk, simulating the approval or review process.

## 4. Problem Statement
The volume of online transactions makes manual review impossible. Existing rule-based systems generate high false-positive rates, blocking genuine customers. There is a need for an automated, self-learning system that can minimize false positives while maintaining high detection rates (Recall) for actual fraud.

## 5. Objectives
- To develop a Machine Learning model capable of identifying fraudulent patterns.
- To handle highly imbalanced transaction datasets.
- To build a web interface for real-time transaction analysis.
- To provide explainable risk factors alongside predictions.

## 6. Existing System
Existing rule-based systems rely on static thresholds (e.g., "block any transaction over $10,000"). They require constant manual updating and cannot detect complex, non-linear relationships between variables (e.g., a small transaction amount that is suspicious because of the time and location combined).

## 7. Proposed System
The proposed system uses a Random Forest Classifier trained on historical data. It evaluates multiple factors simultaneously and assigns a continuous probability score, allowing for granular risk management (Low, Medium, High) rather than a simple binary block/allow.

## 8. Literature/Background
Machine Learning (ML) has become the industry standard for fraud detection. Algorithms like Logistic Regression, Decision Trees, and Random Forests are commonly used. Random Forest is particularly favored for tabular financial data due to its robustness against overfitting and lack of assumptions regarding data distribution.

## 9. System Requirements
- **Software:** Python 3.x, Flask, SQLite, Scikit-Learn, HTML/CSS, Modern Web Browser.
- **Hardware:** standard PC/Laptop (Minimum 4GB RAM, Intel i3/Ryzen 3).

## 10. System Architecture
```text
User Input -> Flask Web App -> Preprocessing Module (StandardScaler/OneHotEncoder) 
-> Random Forest Model -> Risk Score Calculation -> Flask Web App -> Results UI
```

## 11. Dataset
A synthetic dataset containing 2000 records was generated for demonstration purposes, mimicking real-world transaction patterns. It includes features like amount, transaction_type, time, device_type, and location.

## 12. Data Preprocessing
- Missing values (if any) are imputed.
- Numerical features are scaled using `StandardScaler`.
- Categorical features are encoded using `OneHotEncoder`.
- The dataset is split into 80% training and 20% testing sets.

## 13. Machine Learning Algorithms
- **Random Forest:** Chosen for its ensemble approach, high accuracy, and ability to output probability scores.
- **SMOTE:** Applied to the training data to handle the severe class imbalance between genuine and fraudulent transactions.

## 14. Model Evaluation
The model is evaluated using Accuracy, Precision, Recall, and F1-Score. In fraud detection, **Recall** is prioritized because failing to detect fraud (False Negative) is more costly than mistakenly flagging a genuine transaction (False Positive).

## 15. Database Design
The system uses SQLite with two main tables:
- `users`: Stores user credentials securely (hashed passwords).
- `transactions`: Stores historical scans, input features, predicted risk scores, and statuses.

## 16. Results
The trained Random Forest model successfully learned the injected patterns of the synthetic dataset, achieving high precision and recall. The web interface correctly loads the serialized model and processes live inputs in milliseconds.

## 17. Advantages
- Fast, real-time prediction.
- Reduces manual review workload.
- Scalable architecture.
- Explainable AI factors provided to the user.

## 18. Limitations
- The model relies on the quality of historical data.
- The current dataset is synthetic.
- Does not connect to live banking networks.

## 19. Future Scope
- Integration with real-time streaming technologies like Kafka.
- Implementation of Deep Learning (Neural Networks) for more complex pattern recognition.
- Using Graph Neural Networks (GNNs) to map relationships between fraudulent accounts.

## 20. Conclusion
This project successfully demonstrates the application of Machine Learning in FinTech for fraud detection. By combining a robust Random Forest backend with an intuitive Flask frontend, it serves as a complete prototype for automated risk analysis systems.
