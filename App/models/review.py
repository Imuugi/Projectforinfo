from App.database import db
from datetime import datetime
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment_listings.id'), nullable=False)

    def __init__(self,content,rating,tenant_id,apartment_id):
        self.content = content
        self.rating = rating
        self.tenant_id = tenant_id
        self.apartment_id = apartment_id
