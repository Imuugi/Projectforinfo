from App.database import db
from datetime import datetime
class TenantVerification(db.Model):
    __tablename__ = 'tenant_verifications'

    id = db.Column(db.Integer,primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'), primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), primary_key=True)
    apartment_id = db.Column(db.Integer,db.ForeignKey('apartment_listings.id'),primary_key=True)
    verified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,landlord_id,tenant_id,apartment_id):
        self.landlord_id = landlord_id
        self.tenant_id = tenant_id
        self.apartment_id = apartment_id

        