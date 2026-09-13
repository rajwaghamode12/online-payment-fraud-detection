# VIVA Questions and Answers

**1. What is payment fraud?**
Payment fraud is any false or illegal transaction completed by a cybercriminal, usually by stealing credit card numbers or banking credentials.

**2. Why is machine learning used for fraud detection?**
Machine learning algorithms can analyze thousands of transactions in milliseconds, finding hidden patterns of fraud that humans or simple rule-based systems would miss.

**3. What is supervised learning?**
Supervised learning is a type of machine learning where the model is trained on a labeled dataset (data that already contains the answer, like "Fraud" or "Genuine").

**4. What is Random Forest?**
Random Forest is an ensemble learning method that creates multiple decision trees during training and merges their outputs to get a more accurate and stable prediction.

**5. Why did you choose Random Forest?**
Random Forest is highly accurate, handles non-linear data well, provides feature importance, and is less prone to overfitting compared to a single Decision Tree.

**6. What is class imbalance?**
In fraud detection, 99% of transactions are genuine and only 1% are fraud. This imbalance makes the model biased towards predicting "Genuine" to achieve high accuracy.

**7. What is SMOTE?**
SMOTE stands for Synthetic Minority Over-sampling Technique. It generates synthetic examples of the minority class (Fraud) so the model has balanced data to learn from.

**8. What is precision?**
Out of all the transactions the model predicted as Fraud, how many were actually Fraud. 

**9. What is recall?**
Out of all the actual Fraud transactions, how many did the model correctly identify. In fraud detection, high recall is crucial.

**10. What is F1-score?**
The harmonic mean of precision and recall. It provides a single score that balances both concerns.

**11. What is a confusion matrix?**
A table that describes the performance of a classification model, showing True Positives, True Negatives, False Positives, and False Negatives.

**12. What is a false positive?**
When the model predicts a transaction is Fraud, but it is actually Genuine. (An annoyance to the customer).

**13. What is a false negative?**
When the model predicts a transaction is Genuine, but it is actually Fraud. (A financial loss to the bank).

**14. What is feature engineering?**
The process of creating new input features from existing data to improve model performance, such as extracting the "hour of day" from a timestamp.

**15. Why is accuracy not enough to evaluate a fraud model?**
If 99% of transactions are genuine, a model that simply guesses "Genuine" every time will be 99% accurate, but it will catch 0 frauds. Thus, accuracy is misleading in imbalanced datasets.

**16. What is Flask?**
Flask is a lightweight web application framework for Python, used here to build the backend server and connect the ML model to the web interface.

**17. Why use SQLite?**
SQLite is a lightweight, serverless, file-based database that requires no configuration, making it perfect for demonstration and college projects.

**18. How does the prediction work in your system?**
When a user submits a form, the data is scaled, encoded, and passed to the saved `fraud_model.pkl` Random Forest model, which outputs a probability of fraud.

**19. How is the risk score generated?**
The machine learning model outputs a probability between 0.0 and 1.0. We multiply this by 100 to get a Risk Score from 0 to 100.

**20. How are the risk categories defined?**
In this demo: 0-30 is Low Risk, 31-70 is Medium Risk, and 71-100 is High Risk.

**21. What happens when a transaction is High Risk?**
The system flags it as "Suspicious", blocks the demo payment, and suggests it be sent for manual review.

**22. Are the credit card details processed safely?**
This is a simulation. We do not collect real credit card numbers, CVVs, or OTPs, so there is no real financial risk.

**23. How do you handle categorical variables?**
We use One-Hot Encoding via Scikit-Learn's `OneHotEncoder` to convert text categories (like Device Type) into numerical format.

**24. How do you handle numerical variables?**
We use `StandardScaler` to normalize numerical values (like amount and balance) so features with large numbers don't dominate the model.

**25. How do you save the trained model?**
Using the `joblib` library, which serializes the Python objects (`fraud_model.pkl` and `preprocessor.pkl`) to disk.

**26. Why do you save the preprocessor separately?**
The exact same scaling and encoding rules applied during training must be applied to new, single transactions during prediction.

**27. What are the limitations of your project?**
The dataset is synthetic, the system does not integrate with real banking APIs, and real-world fraud patterns change rapidly requiring continuous model retraining.

**28. What is the future scope?**
Integrating Deep Learning, using real-world streaming data with Apache Kafka, and adding a real payment gateway API for testing.

**29. What is Cross-Site Request Forgery (CSRF)?**
A web vulnerability. While not heavily emphasized in this demo, real systems use CSRF tokens to ensure form submissions come from the legitimate site.

**30. How is the Admin dashboard useful?**
It gives a macro view of the system, allowing administrators to see fraud trends, review flagged transactions, and monitor the AI model's performance over time.
