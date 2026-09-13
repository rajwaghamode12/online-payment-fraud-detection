def calculate_risk_score(probability):
    """
    Converts ML model probability (0-1) to a risk score (0-100)
    and categorizes it.
    """
    score = int(probability * 100)
    
    if score <= 30:
        category = 'LOW RISK'
        status = 'APPROVED'
        color = 'success'
    elif score <= 70:
        category = 'MEDIUM RISK'
        status = 'REVIEW'
        color = 'warning'
    else:
        category = 'HIGH RISK'
        status = 'REJECTED/REVIEW'
        color = 'danger'
        
    return score, category, status, color

def generate_reasons(transaction_data):
    """
    Generates explainable reasons for a high risk score based on the input data.
    """
    reasons = []
    
    if float(transaction_data.get('amount', 0)) > 25000:
        reasons.append("Unusually high transaction amount")
        
    time = int(transaction_data.get('transaction_time', 12))
    if time < 6 or time > 23:
        reasons.append("Unusual transaction time (late night/early morning)")
        
    if int(transaction_data.get('new_device', 0)) == 1:
        reasons.append("New device detected")
        
    if int(transaction_data.get('unusual_location', 0)) == 1:
        reasons.append("Unusual location for this user")
        
    if int(transaction_data.get('previous_transactions', 10)) < 2:
        reasons.append("New account with very few previous transactions")
        
    if not reasons:
        reasons.append("Multiple minor anomalies detected by AI model")
        
    return reasons
