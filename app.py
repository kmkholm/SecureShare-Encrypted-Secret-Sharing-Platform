from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import string
from datetime import datetime, timedelta
import segno
from schema import db, init_db, User, Secret

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///share_secret.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return render_template('register.html', error='Username or email already exists')
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session.permanent = True
        
        return redirect('/dashboard')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Secret routes
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    secrets = Secret.query.filter_by(user_id=user_id).all()
    
    return render_template('dashboard.html', secrets=secrets, username=session.get('username'))

@app.route('/create', methods=['GET', 'POST'])
def create_secret():
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        password = request.form.get('password')
        blur_level = int(request.form.get('blur_level', 10))
        expiration = request.form.get('expiration', '0')
        
        # Validate required fields
        if not title or not content or not password:
            return render_template('create.html', error='All fields are required')
        
        # Set expiration date
        expires_at = None
        try:
            expiration_hours = int(expiration)
            if expiration_hours > 0:
                expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
        except ValueError:
            pass
        
        # Generate unique ID
        unique_id = f"sec_{''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))}"
        
        # Create new secret
        new_secret = Secret(
            user_id=session['user_id'],
            title=title,
            content=content,
            blur_level=blur_level,
            expires_at=expires_at,
            unique_id=unique_id
        )
        new_secret.set_password(password)
        
        # Generate QR code
        qr_dir = os.path.join(app.static_folder, 'qrcodes')
        os.makedirs(qr_dir, exist_ok=True)
        
        qr_filename = f"qr_{unique_id}.png"
        qr_path = os.path.join(qr_dir, qr_filename)
        
        # Create QR code using segno
        qr_content = f"{request.host_url}view/{unique_id}"
        qr = segno.make(qr_content, error='l')
        qr.save(qr_path, scale=10, border=4)
        
        # Save QR path
        new_secret.qr_path = f"qrcodes/{qr_filename}"
        
        # Save to database
        db.session.add(new_secret)
        db.session.commit()
        
        return redirect(f'/view/{unique_id}')
    
    return render_template('create.html')

@app.route('/view/<unique_id>', methods=['GET', 'POST'])
def view_secret(unique_id):
    secret = Secret.query.filter_by(unique_id=unique_id).first()
    
    if not secret:
        return render_template('error.html', message='Secret not found')
    
    # Check if secret has expired
    if secret.expires_at and secret.expires_at < datetime.utcnow():
        return render_template('error.html', message='This secret has expired')
    
    if request.method == 'POST':
        password = request.form.get('password')
        
        if secret.check_password(password):
            # Increment view count
            secret.view_count += 1
            db.session.commit()
            
            return render_template('view.html', secret=secret, authenticated=True)
        else:
            return render_template('view.html', secret=secret, authenticated=False, error='Incorrect password')
    
    return render_template('view.html', secret=secret, authenticated=False)

# Main routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/api/auth/check')
def check_auth():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'success': True,
                'user': user.to_dict()
            })
    
    return jsonify({
        'success': False,
        'error': 'Not logged in'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
