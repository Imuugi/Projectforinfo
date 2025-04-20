from App.database import db
from datetime import datetime
class VerificationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,tenant_id,landlord_id,apartment_id):
        self.tenant_id = tenant_id
        self.landlord_id = landlord_id
        self.apartment_id = apartment_id

