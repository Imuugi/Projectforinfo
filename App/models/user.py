from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default = 'tenant')
    landlord = db.relationship('Landlord', backref='user', uselist=False)
    tenant = db.relationship('Tenant', backref='user', uselist=False)

    def __init__(self, username, password, user_type=None):
        self.username = username
        self.set_password(password)
        self.user_type = user_type if user_type else 'tenant'

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

