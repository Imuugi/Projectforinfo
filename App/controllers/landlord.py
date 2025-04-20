from App.models import Landlord,ApartmentListing,TenantVerification
from App.database import db

def create_listing(title,description,location,amenities,price,landlord_id,image=None):
    newlisting = ApartmentListing(title=title,description=description,location=location,amenities=amenities,price=price,landlord_id=landlord_id,image=image)
    db.session.add(newlisting)
    db.session.commit()
    return newlisting

def view_listings(landlord_id):
    listings = ApartmentListing.query.filter_by(landlord_id = landlord_id).all()
    return listings

def verify_tenant(landlord_id,tenant_id,apartment_id):
    verifiedtenant = TenantVerification(landlord_id = landlord_id,tenant_id = tenant_id,apartment_id= apartment_id)
    db.session.add(verifiedtenant)
    db.session.commit()
    return verifiedtenant

def view_verified_tenants(landlord_id):
    verifiedtenants = TenantVerification.query.filter_by(landlord_id = landlord_id).all()
    return verifiedtenants