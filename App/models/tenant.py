from App.database import db
from .user import User

class Tenant(User):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    is_verified = db.Column(db.Boolean, default=False)

   
    reviews = db.relationship('Review', backref='tenant', lazy=True)
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.user_type = "tenant"
