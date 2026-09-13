import pandas as pd
import numpy as np
import os
import random

def generate_dataset(num_records=2000, fraud_ratio=0.08):
    np.random.seed(42)
    random.seed(42)
    
    data = []
    num_fraud = int(num_records * fraud_ratio)
    num_genuine = num_records - num_fraud
    
    types = ['UPI', 'Credit Card', 'Debit Card', 'Net Banking']
    locations = ['Same City', 'Different City', 'Different Country']
    devices = ['Mobile', 'Desktop', 'Tablet']
    
    # Generate Genuine
    for _ in range(num_genuine):
        amount = round(np.random.lognormal(mean=7.0, sigma=1.0), 2)  # Normal small amounts
        trans_type = random.choice(types)
        trans_time = random.randint(6, 23)  # Mostly daytime
        sender_bal = round(amount + np.random.uniform(100, 50000), 2)
        receiver_bal = round(np.random.uniform(0, 100000), 2)
        location = random.choices(locations, weights=[0.8, 0.19, 0.01])[0]
        device = random.choice(devices)
        prev_trans = random.randint(10, 500)
        new_dev = 0 if random.random() > 0.1 else 1
        unusual_loc = 0 if location == 'Same City' else (1 if random.random() > 0.5 else 0)
        
        data.append([amount, trans_type, trans_time, sender_bal, receiver_bal, 
                     location, device, prev_trans, new_dev, unusual_loc, 0])
                     
    # Generate Fraud
    for _ in range(num_fraud):
        amount = round(np.random.lognormal(mean=9.5, sigma=1.5), 2) # Higher amounts
        trans_type = random.choice(types)
        trans_time = random.choices([random.randint(0, 5), random.randint(6, 23)], weights=[0.7, 0.3])[0] # Mostly night time
        sender_bal = round(np.random.uniform(0, 10000), 2)
        receiver_bal = round(np.random.uniform(10000, 500000), 2)
        location = random.choices(locations, weights=[0.1, 0.4, 0.5])[0]
        device = random.choice(devices)
        prev_trans = random.randint(0, 5) # New accounts
        new_dev = 1 if random.random() > 0.1 else 0 # Usually new device
        unusual_loc = 1 if location != 'Same City' else (1 if random.random() > 0.2 else 0)
        
        data.append([amount, trans_type, trans_time, sender_bal, receiver_bal, 
                     location, device, prev_trans, new_dev, unusual_loc, 1])
                     
    columns = [
        'amount', 'transaction_type', 'transaction_time', 'sender_balance', 
        'receiver_balance', 'location', 'device_type', 'previous_transactions', 
        'new_device', 'unusual_location', 'Fraud'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    df = df.sample(frac=1).reset_index(drop=True) # Shuffle
    
    # Save
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'payment_fraud.csv')
    df.to_csv(file_path, index=False)
    print(f"Dataset generated at {file_path} with {len(df)} records (Fraud ratio: {df['Fraud'].mean():.2%})")

if __name__ == '__main__':
    generate_dataset()
