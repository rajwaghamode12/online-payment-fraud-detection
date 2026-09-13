from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user') # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50))
    transaction_time = db.Column(db.Integer) # Hour of day
    sender_balance = db.Column(db.Float)
    receiver_balance = db.Column(db.Float)
    location = db.Column(db.String(100))
    device_type = db.Column(db.String(50))
    previous_transactions = db.Column(db.Integer)
    new_device = db.Column(db.Integer)
    unusual_location = db.Column(db.Integer)
    
    fraud_probability = db.Column(db.Float)
    risk_score = db.Column(db.Integer)
    prediction = db.Column(db.String(20)) # 'Genuine' or 'Fraud'
    status = db.Column(db.String(20)) # 'LOW RISK', 'MEDIUM RISK', 'HIGH RISK'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
