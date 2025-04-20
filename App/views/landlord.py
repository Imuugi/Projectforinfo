from flask import Blueprint, render_template, request
from App.controllers import (view_listings, create_listing, verify_tenant,delete_apartment)
from App.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models import ApartmentListing
from App.controllers import verify_tenant,delete_request
landlord_views = Blueprint('landlord_views',__name__,template_folder='../templates')

@landlord_views.route('/viewlisting')
@jwt_required()
def list_apartments():
    username = get_jwt_identity()
    if username:
        user = User.query.filter_by(username=username).first()
        if user and user.landlord:
            listings = ApartmentListing.query.filter_by(landlord_id=user.landlord.id).all()
            return render_template('viewlisting.html', listings=listings)
    return "Please login as a landlord", 401

@landlord_views.route('/landlord/create-listing', methods=['GET', 'POST'])
@jwt_required()
def create_listing_page():
    if request.method == 'POST':
        landlord_id = get_jwt_identity()
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        amenities = request.form['amenities']
        price = float(request.form['price'])

        listing = create_listing(title, description, location, amenities, price, landlord_id)
        return redirect(url_for('landlord_views.list_apartments'))

    return render_template('index.html')


@landlord_views.route('/landlord/delete-listing',methods = ['GET','POST'])
@jwt_required()
def delete_listing():
    landlord_id = get_jwt_identity()
    
    if request.method == 'POST':
        listing_id = request.form.get('listing_id')

        if not listing_id:
            return "Missing listing ID", 400
        deleted_listing = delete_apartment(landlord_id, listing_id)

        if deleted_listing:
            return "Listing deleted successfully!", 200
        else:
            return "Listing not found or unauthorized", 404

    return render_template('index.html')

@landlord_views.route('/landlord/verifytenant', methods = ['GET','POST'])
@jwt_required()
def verify_tenant():
    if request.method == 'POST':
        landlord_id = get_jwt_identity()
        tenant_id = request.form.get('tenant_id')
        verify_tenant(landlord_id,tenant_id)
        return "Tenant verified", 200

    return render_template('index.html')

@landlord_views.route('/ldsearch')
def search():
    query = request.args.get('query')
    filter_by = request.args.get('filter')

    if not query or not filter_by:
        # maybe flash a message or redirect back
        return "Missing search parameters", 400

    if filter_by == 'location':
        results = ApartmentListing.query.filter(ApartmentListing.location.ilike(f"%{query}%")).all()
    elif filter_by == 'amenities':
        results = ApartmentListing.query.filter(ApartmentListing.amenities.ilike(f"%{query}%")).all()
    else:
        results = []

    return render_template('landlord_search_results.html', results=results, query=query, filter_by=filter_by)



@landlord_views.route('/landlord/accept_request' ,methods=['GET', 'POST'])
@jwt_required()
def accept_request():
    if request.method == 'POST':
        request_id = request.form['request_id']
        tenant_id = request.form['tenant_id']
        apartment_id = request.form['apartment_id']
        landlord_id = request.form['landlord_id']
        verify_tenant(landlord_id,tenant_id,apartment_id)
        delete_request(request_id)
        return render_template('landlordhome.html')

       
@landlord_views.route('/landlord/decline_request',methods=['GET', 'POST'])
@jwt_required()
def decline_request():
    request_id = request.form['request_id']
    delete_request(request_id)
    return render_template('landlordhome.html', listings=ApartmentListing.query.all())
