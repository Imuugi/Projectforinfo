from .user import create_user
from App.database import db
from App.models import Landlord,Tenant,Review,ApartmentListing

def initialize():
    db.drop_all()
    db.create_all()
    tenant1 = Tenant('bob', 'bobpass')

    # Create some dummy landlords
    landlord1 = Landlord(username="landlord_john", password="password123")
    landlord2 = Landlord(username="landlord_jane", password="securepass456")

    # Add landlords to the database
    db.session.add(landlord1)
    db.session.add(landlord2)
    db.session.commit()

    # Create dummy apartment listings
    listing1 = ApartmentListing(
        title="Cozy Studio in Downtown",
        description="A cozy studio apartment perfect for young professionals.",
        location="Downtown",
        amenities="WiFi, Air Conditioning, Gym Access",
        price=1200.00,
        landlord_id=landlord1.id,
        image="sample_images/apartment1.jpg"
    )
    listing2 = ApartmentListing(
        title="Spacious 2 Bedroom Apartment",
        description="Large two-bedroom unit near the park. Pet-friendly!",
        location="Uptown",
        amenities="Washer/Dryer, Pet Friendly, Parking",
        price=1800.00,
        landlord_id=landlord1.id,
        image="sample_images/apartment2.jpg"
    )

    listing3 = ApartmentListing(
        title="Modern Loft",
        description="Open concept loft with modern amenities.",
        location="Midtown",
        amenities="WiFi, Rooftop Pool, Gym Access",
        price=1500.00,
        landlord_id=landlord2.id,
        image="sample_images/apartment3.jpg"
    )

    db.session.add(listing1)
    db.session.add(listing2)
    db.session.add(listing3)
    db.session.commit()


    bill = Tenant(username="bill", password="billpass")
    db.session.add(bill)
    db.session.commit()

   
    review1 = Review(
        rating=4,
        content="Great place, very cozy and close to everything!",
        tenant_id=bill.id,
        apartment_id=listing1.id
    )

    review2 = Review(
        rating=5,
        content="Amazing apartment, lots of space and my dog loved it!",
       tenant_id=bill.id,
        apartment_id=listing2.id
    )

    review3 = Review(
        rating=3,
        content="Nice loft but could be cleaner.",
        tenant_id=bill.id,
        apartment_id=listing3.id
    )
     
    db.session.add(review1)
    db.session.add(review2)
    db.session.add(review3)
    db.session.commit()
    print("Reviews Added")

   
