A secure, privacy-focused web application for sharing sensitive information with password protection, automatic expiration, and QR code generation. Built with Flask and designed for confidential message sharing in professional and personal environments.
🎯 Project Overview
SecureShare addresses the critical need for secure information exchange in our digital world. Whether sharing API keys, passwords, personal messages, or sensitive documents, this platform ensures your data remains protected with multiple layers of security.
Key Security Features
FeatureDescriptionSecurity BenefitPassword ProtectionIndividual password per secretAccess controlAuto-ExpirationTime-based secret deletionLimited exposure windowEncrypted StorageHashed passwords in databaseData protection at restSession SecurityHTTPOnly cookies, CSRF protectionSession hijacking preventionQR Code GenerationSecure sharing without URLsConvenient mobile accessView TrackingMonitor secret accessUsage transparencyBlur ProtectionVisual privacy on shared screensShoulder surfing prevention
🏗️ Architecture Overview
Technology Stack
pythonBackend Framework: Flask 2.x
Database: SQLite with SQLAlchemy ORM
Authentication: Werkzeug Security (bcrypt)
QR Generation: Segno library
Session Management: Flask-Session
Frontend: HTML5 + CSS3 + JavaScript
Security Architecture
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Client    │    │   Flask App      │    │   SQLite DB     │
│                 │    │                  │    │                 │
│ • HTTPS Only    │◄──►│ • Password Hash  │◄──►│ • Encrypted     │
│ • Secure Forms  │    │ • Session Mgmt   │    │   Storage       │
│ • QR Scanner    │    │ • CSRF Protection│    │ • User Auth     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
🚀 Quick Start
Prerequisites
bash# Python 3.8+ required
python --version

# Install dependencies
pip install flask sqlalchemy werkzeug segno pillow

# Or use requirements file
pip install -r requirements.txt
Installation & Setup
bash# Clone the repository
git clone https://github.com/yourusername/secureshare.git
cd secureshare

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Run the application
python app.py
First Run

Navigate to http://localhost:5000
Register a new account
Create your first encrypted secret
Share via QR code or direct link

📁 Project Structure
secureshare/
├── app.py                    # Main Flask application
├── schema.py                 # Database models and initialization
├── requirements.txt          # Python dependencies
├── README.md                # This documentation
├── static/                  # Static assets
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   ├── qrcodes/           # Generated QR codes
│   └── images/            # UI assets
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Landing page
│   ├── login.html         # User authentication
│   ├── register.html      # User registration
│   ├── dashboard.html     # User dashboard
│   ├── create.html        # Create secret form
│   ├── view.html          # View secret page
│   └── error.html         # Error display
├── instance/              # Instance-specific config
│   └── share_secret.db    # SQLite database
└── logs/                  # Application logs
    └── app.log
🔧 Core Functionality
User Management
python# User Registration & Authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Validates unique username/email
    # Hashes passwords with Werkzeug
    # Creates secure sessions
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Authenticates against hashed passwords
    # Establishes secure sessions
    # Implements session persistence
Secret Creation & Management
python# Create Encrypted Secret
@app.route('/create', methods=['GET', 'POST'])
def create_secret():
    # Generates unique secret IDs
    # Applies password protection
    # Sets expiration timers
    # Creates QR codes for sharing
    
# Secure Secret Access  
@app.route('/view/<unique_id>', methods=['GET', 'POST'])
def view_secret(unique_id):
    # Validates secret existence
    # Checks expiration status
    # Verifies password authentication
    # Tracks view statistics
Advanced Features
Auto-Expiration System
pythonexpires_at = datetime.utcnow() + timedelta(hours=expiration_hours)

# Automatic cleanup on access
if secret.expires_at and secret.expires_at < datetime.utcnow():
    return render_template('error.html', message='Secret has expired')
QR Code Generation
pythonqr_content = f"{request.host_url}view/{unique_id}"
qr = segno.make(qr_content, error='l')
qr.save(qr_path, scale=10, border=4)
Blur Protection
pythonblur_level = int(request.form.get('blur_level', 10))
# Applies CSS blur filter for visual privacy
🛡️ Security Implementation
Password Security
python# Werkzeug password hashing (bcrypt-based)
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
Session Security
python# Secure session configuration
app.config['SESSION_COOKIE_HTTPONLY'] = True      # Prevent XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'     # CSRF protection  
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
Database Security
python# SQLAlchemy with parameterized queries (SQL injection prevention)
user = User.query.filter_by(username=username).first()
secret = Secret.query.filter_by(unique_id=unique_id).first()
📊 Database Schema
User Model
pythonclass User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    secrets = db.relationship('Secret', backref='owner', lazy=True)
Secret Model
pythonclass Secret(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    unique_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    blur_level = db.Column(db.Integer, default=10)
    expires_at = db.Column(db.DateTime, nullable=True)
    view_count = db.Column(db.Integer, default=0)
    qr_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
🎨 User Interface Features
Dashboard Overview

Secret Management: View all created secrets
Quick Actions: Create, edit, delete secrets
Statistics: View counts, expiration status
QR Code Access: Download or display QR codes

Secret Creation Form

Title & Content: Rich text input for secret data
Password Protection: Custom password for each secret
Expiration Options: 1hr, 24hr, 7 days, or custom
Blur Level: Adjustable visual privacy (0-20px)
QR Generation: Automatic QR code creation

Secret Viewing Interface

Password Prompt: Secure access control
Blur Protection: Configurable content blurring
View Tracking: Access statistics display
Expiration Warning: Time remaining indicator

⚙️ Configuration Options
Application Settings
python# Core Flask Configuration
class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///share_secret.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # Enable in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
Production Deployment
python# Production-ready configuration
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
🚀 Deployment Options
Local Development
bash# Development server
python app.py

# Access at http://localhost:5000
Production Deployment
Using Gunicorn (Recommended)
bash# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# With SSL (production)
gunicorn -w 4 -b 0.0.0.0:443 --certfile=cert.pem --keyfile=key.pem app:app
Docker Deployment
dockerfileFROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
Nginx Configuration
nginxserver {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
📱 API Documentation
Authentication Endpoints
python# Check Authentication Status
GET /api/auth/check
Response: {
    "success": true,
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    }
}
Future API Extensions
python# Planned REST API endpoints
GET    /api/secrets          # List user secrets
POST   /api/secrets          # Create new secret
GET    /api/secrets/:id      # Get secret details
DELETE /api/secrets/:id      # Delete secret
POST   /api/secrets/:id/view # Access secret with password
🔍 Security Best Practices
For Users

Strong Passwords: Use unique, complex passwords for each secret
Limited Sharing: Share QR codes and links only with intended recipients
Expiration Awareness: Set appropriate expiration times for sensitive data
Secure Networks: Access only over HTTPS and trusted networks

For Administrators

HTTPS Only: Always use SSL/TLS in production
Regular Updates: Keep dependencies updated for security patches
Backup Strategy: Regular database backups with encryption
Monitoring: Log access patterns and failed authentication attempts

🐛 Troubleshooting
Common Issues

Database Connection Errors
bash# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

QR Code Generation Fails
bash# Ensure static directory exists
mkdir -p static/qrcodes
chmod 755 static/qrcodes

Session Issues
python# Clear browser cookies and restart Flask app
# Check SECRET_KEY is set consistently

Permission Errors
bash# Fix file permissions
chmod -R 755 static/
chmod 644 instance/share_secret.db


🔄 Future Enhancements
Planned Features

File Upload Support: Share documents and images securely
Mobile App: Native iOS/Android applications
API Integration: RESTful API for third-party integrations
Advanced Analytics: Detailed usage statistics and reporting
Team Management: Organization accounts with role-based access
Encrypted Messaging: Real-time secure chat functionality

Technical Improvements

Redis Integration: Session storage and caching
Email Notifications: Expiration alerts and access notifications
Two-Factor Authentication: Enhanced security with TOTP
Audit Logging: Comprehensive security event logging
Database Encryption: Full database encryption at rest

🤝 Contributing
Development Setup
bash# Clone repository
git clone https://github.com/yourusername/secureshare.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black app.py schema.py
flake8 app.py schema.py
Contribution Guidelines

Fork the repository
Create a feature branch (git checkout -b feature/enhanced-security)
Make changes with comprehensive tests
Ensure security best practices
Submit pull request with detailed description

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Flask Community for the excellent web framework
Werkzeug Team for security utilities
Segno Library for QR code generation
SQLAlchemy for robust ORM functionality
Security Research Community for best practices guidance

⚠️ Security Disclaimer
Important Notes

Production Security: This application requires HTTPS for production use
Data Sensitivity: Users are responsible for the sensitivity of shared content
Regular Updates: Keep all dependencies updated for security patches
Compliance: Ensure compliance with local data protection regulations
Penetration Testing: Regular security audits recommended for production deployments

Responsible Disclosure
If you discover security vulnerabilities, please report them responsibly:

Email: kmkhol01@gmail.com
Include detailed reproduction steps
Allow 90 days for patch development before public disclosure
