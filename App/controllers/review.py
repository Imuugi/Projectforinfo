from App.models import Review,ApartmentListing
from App.database import db

def get_reviews(apartment_id):
    reviews = Review.query.filter_by(apartment_id = apartment_id).all()
    return reviews

def delete_review(tenant_id,review_id):
    review = Review.query.get(review_id)
    if not review or review.tenant_id != tenant_id:
        return None
    db.session.delete(review)
    db.session.commit()
    