import os
import uuid
import joblib
import json
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func

from config import Config
from database.models import db, User, Transaction
from utils.preprocessing import format_input_for_model
from utils.risk_scoring import calculate_risk_score, generate_reasons

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Load ML Model and Preprocessor
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'model', 'fraud_model.pkl')
preprocessor_path = os.path.join(base_dir, 'model', 'preprocessor.pkl')

# Global variables for model
model = None
preprocessor = None

def load_ml_components():
    global model, preprocessor
    try:
        if os.path.exists(model_path) and os.path.exists(preprocessor_path):
            model = joblib.load(model_path)
            preprocessor = joblib.load(preprocessor_path)
            print("ML Model and Preprocessor loaded successfully.")
    except Exception as e:
        print(f"Error loading ML components: {e}")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables and initial admin
with app.app_context():
    db.create_all()
    # Create demo admin if not exists
    admin_exists = User.query.filter_by(email='admin@demo.com').first()
    if not admin_exists:
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(name='Admin', email='admin@demo.com', password_hash=hashed_password, role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please log in.', 'danger')
            return redirect(url_for('register'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login. Email or password is incorrect.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
        
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()
    
    total = len(transactions)
    genuine = len([t for t in transactions if t.prediction == 'Genuine'])
    suspicious = len([t for t in transactions if t.status == 'MEDIUM RISK'])
    fraud = len([t for t in transactions if t.prediction == 'Fraud'])
    
    recent_transactions = transactions[:5]
    
    return render_template('dashboard.html', 
                           total=total, genuine=genuine, 
                           suspicious=suspicious, fraud=fraud,
                           recent_transactions=recent_transactions)

@app.route('/check-transaction', methods=['GET', 'POST'])
@login_required
def check_transaction():
    if request.method == 'POST':
        try:
            # Ensure model is loaded
            if model is None or preprocessor is None:
                load_ml_components()
            if model is None:
                flash("Error: Machine Learning model is not available.", "danger")
                return redirect(url_for('check_transaction'))
                
            # Collect data
            data = request.form.to_dict()
            
            # Preprocess
            df = format_input_for_model(data)
            X_processed = preprocessor.transform(df)
            
            # Predict
            prob = model.predict_proba(X_processed)[0][1] # Probability of fraud (class 1)
            pred_class = model.predict(X_processed)[0]
            
            prediction = 'Fraud' if pred_class == 1 else 'Genuine'
            score, category, payment_status, color = calculate_risk_score(prob)
            reasons = generate_reasons(data) if category in ['MEDIUM RISK', 'HIGH RISK'] else []
            
            # Save transaction
            tx_id = "TXN" + str(uuid.uuid4())[:8].upper()
            tx = Transaction(
                transaction_id=tx_id,
                user_id=current_user.id,
                amount=float(data['amount']),
                transaction_type=data['transaction_type'],
                transaction_time=int(data['transaction_time']),
                sender_balance=float(data['sender_balance']),
                receiver_balance=float(data['receiver_balance']),
                location=data['location'],
                device_type=data['device_type'],
                previous_transactions=int(data['previous_transactions']),
                new_device=int(data['new_device']),
                unusual_location=int(data['unusual_location']),
                fraud_probability=prob,
                risk_score=score,
                prediction=prediction,
                status=category
            )
            db.session.add(tx)
            db.session.commit()
            
            session['last_result'] = {
                'tx_id': tx_id,
                'score': score,
                'category': category,
                'status': payment_status,
                'color': color,
                'prob': round(prob * 100, 2),
                'reasons': reasons
            }
            return redirect(url_for('result'))
            
        except ValueError:
            flash('Invalid input. Please enter valid numerical values.', 'danger')
        except Exception as e:
            flash(f'Prediction error. Unable to analyze this transaction.', 'danger')
            
    return render_template('check_transaction.html')

@app.route('/transaction-result')
@login_required
def result():
    result_data = session.get('last_result')
    if not result_data:
        return redirect(url_for('dashboard'))
    return render_template('result.html', result=result_data)

@app.route('/transactions')
@login_required
def transactions():
    status_filter = request.args.get('status')
    
    query = Transaction.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    txs = query.order_by(Transaction.created_at.desc()).all()
    return render_template('transactions.html', transactions=txs)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('dashboard'))
        
    all_txs = Transaction.query.all()
    total = len(all_txs)
    genuine = len([t for t in all_txs if t.prediction == 'Genuine'])
    suspicious = len([t for t in all_txs if t.status == 'MEDIUM RISK'])
    fraud = len([t for t in all_txs if t.prediction == 'Fraud'])
    
    total_amount = sum([t.amount for t in all_txs])
    fraud_pct = round((fraud / total * 100) if total > 0 else 0, 2)
    
    recent_suspicious = Transaction.query.filter(Transaction.status.in_(['MEDIUM RISK', 'HIGH RISK'])).order_by(Transaction.created_at.desc()).limit(5).all()
    
    # Load model performance if exists
    perf_path = os.path.join(base_dir, 'model', 'model_performance.json')
    model_perf = None
    if os.path.exists(perf_path):
        with open(perf_path, 'r') as f:
            model_perf = json.load(f)
            
    return render_template('admin.html', 
                           total=total, genuine=genuine, 
                           suspicious=suspicious, fraud=fraud,
                           total_amount=total_amount, fraud_pct=fraud_pct,
                           recent_suspicious=recent_suspicious,
                           model_perf=model_perf)

@app.route('/admin/transactions')
@login_required
def admin_transactions():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
        
    txs = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return render_template('transactions.html', transactions=txs, is_admin=True)

if __name__ == '__main__':
    load_ml_components()
    app.run(debug=True)
