import pandas as pd

def format_input_for_model(data_dict):
    """
    Converts raw form data into a pandas DataFrame suitable for the preprocessor.
    """
    df = pd.DataFrame([{
        'amount': float(data_dict['amount']),
        'transaction_type': data_dict['transaction_type'],
        'transaction_time': int(data_dict['transaction_time']),
        'sender_balance': float(data_dict['sender_balance']),
        'receiver_balance': float(data_dict['receiver_balance']),
        'location': data_dict['location'],
        'device_type': data_dict['device_type'],
        'previous_transactions': int(data_dict['previous_transactions']),
        'new_device': int(data_dict['new_device']),
        'unusual_location': int(data_dict['unusual_location'])
    }])
    return df
