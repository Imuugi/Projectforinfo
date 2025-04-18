from App.models import ApartmentListing
from App.database import db

def get_all_apartments():
    return ApartmentListing.query.all()
    

def location_search(location):
    return ApartmentListing.query.filter_by(location = location).all()

def amenities_search(amenity):
    return ApartmentListing.query.filter(ApartmentListing.amenities.like(f"%{amenity}%")).all()


def delete_apartment(apartment_id,landlord_id):
    apartment = ApartmentListing.query.get(apartment_id)

    if not apartment or apartment.landlord_id != landlord_id:
        return None
    
    db.session.delete(apartment)
    db.session.commit()


def update_apartment(apartment_id, title=None, description=None, location=None, amenities=None, price=None):
    apartment = ApartmentListing.query.get(apartment_id)
    if not apartment:
        return None

    if title:
        apartment.title = title
    if description:
        apartment.description = description
    if location:
        apartment.location = location
    if amenities:
        apartment.amenities = amenities
    if price:
        apartment.price = price

    db.session.commit()
    return apartment