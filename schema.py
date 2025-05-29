from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import secrets
import string

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    secrets = db.relationship('Secret', backref='owner', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_admin': self.is_admin
        }

class Secret(db.Model):
    __tablename__ = 'secrets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    blur_level = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0)
    unique_id = db.Column(db.String(50), unique=True, nullable=False)
    qr_path = db.Column(db.String(255))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_unique_id(self):
        alphabet = string.ascii_letters + string.digits
        unique_id = 'sec_' + ''.join(secrets.choice(alphabet) for _ in range(10))
        return unique_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'blur_level': self.blur_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'view_count': self.view_count,
            'unique_id': self.unique_id
        }

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@sharesecret.com',
                is_admin=True
            )
            admin.set_password('1234567')  # Set password to 1234567 as requested
            db.session.add(admin)
            db.session.commit()
