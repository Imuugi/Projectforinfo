from App.database import db
from datetime import datetime
class ApartmentListing(db.Model):
    __tablename__ = 'apartment_listings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    amenities = db.Column(db.Text, nullable=False)  
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String,nullable = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'), nullable=False)
    reviews = db.relationship('Review', backref='apartment', lazy=True)

    def __init__(self,title,description,location,amenities,price,landlord_id,image=None):
        self.title = title
        self.description = description
        self.location = location
        self.amenities = amenities
        self.price = price
        self.landlord_id = landlord_id
        self.image = image