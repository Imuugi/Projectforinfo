from App.models import Landlord
from App.database import db

def create_listing(title,description,location,amenities,price,landlord_id):
    newlisting = ApartmentListing(title,description,location,amenities,price,landlord_id)
    db.session.add(newlisting)
    db.session.commit()
    return newlisting

def view_listings(landlord_id):
    listings = ApartmentListing.query.filter_by(landlord_id = landlord_id).all()
    return listings