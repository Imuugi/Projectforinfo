import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from App.models import Landlord, ApartmentListing
from App.database import db


from App.database import init_db
from App.config import load_config


from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views, setup_admin

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_admin(app)
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    app.app_context().push()
    create_dummy_data()
    return app
def create_dummy_data():
    if Landlord.query.first():
        print("Dummy data already exists.")
        return

    # Create some dummy landlords
    landlord1 = Landlord(username="landlord_john", password="password123")
    landlord2 = Landlord(username="landlord_jane", password="securepass456")

    # Add landlords to the database
    db.session.add(landlord1)
    db.session.add(landlord2)
    db.session.commit()

    # Now create some dummy apartment listings
    listing1 = ApartmentListing(
    title="Cozy Studio in Downtown",
    description="A cozy studio apartment perfect for young professionals.",
    location="Downtown",
    amenities="WiFi, Air Conditioning, Gym Access",
    price=1200.00,
    landlord_id=landlord1.id
)

    listing2 = ApartmentListing(
    title="Spacious 2 Bedroom Apartment",
    description="Large two-bedroom unit near the park. Pet-friendly!",
    location="Uptown",
    amenities="Washer/Dryer, Pet Friendly, Parking",
    price=1800.00,
    landlord_id=landlord1.id
)

    listing3 = ApartmentListing(
    title="Modern Loft",
    description="Open concept loft with modern amenities.",
    location="Midtown",
    amenities="WiFi, Rooftop Pool, Gym Access",
    price=1500.00,
    landlord_id=landlord2.id
)

# Add listings to the database
    db.session.add(listing1)
    db.session.add(listing2)
    db.session.add(listing3)
    db.session.commit()

    print("Dummy landlords and apartment listings created successfully!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_dummy_data()