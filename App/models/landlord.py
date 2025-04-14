from App.database import db
from .user import User


class Landlord(User):
    __tablename__ = 'landlords'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    listings = db.relationship('ApartmentListing', backref='landlord', lazy=True)
    verified_tenants = db.relationship('Tenant', secondary='tenant_verifications', backref='verifying_landlords')

    def __init__(self,username,password):
        self.username = username
        self.set_password(password)
        self.user_type = "landlord"