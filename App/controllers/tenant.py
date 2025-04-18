from App.models import Tenant, Review, TenantVerification, ApartmentListing
from App.database import db

def create_review(tenant_id,content,rating,apartment_id):
    apartment = ApartmentListing.query.get(apartment_id)
    if not apartment:
        return None

    verified = TenantVerification.query.filter_by(landlord_id = apartment.landlord_id).first()

    if not verified:
        return None

    new_review = Review(content = content,rating = rating,tenant_id = tenant_id,apartment_id = apartment_id)
    db.session.add(new_review)
    db.session.commit()
    return new_review
 
def view_reviews(tenant_id):
    reviews = Review.query.filter_by(tenant_id = tenant_id).all()
    return reviews

