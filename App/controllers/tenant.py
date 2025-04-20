from App.models import Tenant, Review, TenantVerification, ApartmentListing
from App.database import db

def create_review(tenant_id,content,rating,apartment_id):
    apartment = ApartmentListing.query.get(apartment_id)
    if not apartment:
        return None

    verified = TenantVerification.query.filter_by(
    landlord_id=apartment.landlord_id,
    apartment_id=apartment.id).first()

    if not verified:

    # Create a verification request
        verification_request = VerificationRequest(
        tenant_id=current_user.id,
        apartment_id=apartment.id,
        landlord_id=apartment.landlord_id
    )
    db.session.add(verification_request)
    db.session.commit()

    flash('You must be verified by the landlord before reviewing this property.', 'info')
    return redirect(url_for('index_views.get_home_page'))

    new_review = Review(content = content,rating = rating,tenant_id = tenant_id,apartment_id = apartment_id)
    db.session.add(new_review)
    db.session.commit()
    return new_review
 
def view_reviews(tenant_id):
    reviews = Review.query.filter_by(tenant_id = tenant_id).all()
    return reviews

