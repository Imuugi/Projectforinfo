from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from App.controllers import (view_listings, create_listing, verify_tenant,delete_apartment)
from App.database import db
from App.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models import ApartmentListing,Landlord,VerificationRequest
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

@landlord_views.route('/createlisting', methods=['GET', 'POST'])
@jwt_required()
def create_listing_page():
    if request.method == 'POST':
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if user and user.landlord:
            title = request.form['title']
            description = request.form['description']
            location = request.form['location']
            amenities = request.form['amenities']
            price = float(request.form['price'])
            
            image = request.files.get('image')
            image_path = None
            if image:
                filename = secure_filename(image.filename)
                filepath = f'App/static/sample_images/{filename}'
                image.save(filepath)
                image_path = f'sample_images/{filename}'
            
            listing = create_listing(title, description, location, amenities, price, user.landlord.id, image_path)
            return redirect(url_for('index_views.landlord_home'))
            
    return render_template('createlisting.html')


@landlord_views.route('/landlord/delete-listing',methods = ['GET','POST'])
@jwt_required()
def delete_listing():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    
    if request.method == 'POST':
        listing_id = request.form.get('listing_id')

        if not listing_id:
            return "Missing listing ID", 400
            
        deleted_listing = delete_apartment(listing_id, user.landlord.id)
        return redirect(url_for('landlord_views.list_apartments'))

    return render_template('createlisting.html')

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



@landlord_views.route('/landlord/accept_request', methods=['GET', 'POST'])
@jwt_required()
def accept_request():
    if request.method == 'POST':
        current_username = get_jwt_identity()
        landlord = Landlord.query.filter_by(username=current_username).first()
        if not landlord:
            return "Unauthorized", 401

        tenant_id = request.form.get('tenant_id')
        apartment_id = request.form.get('apartment_id')
        request_id = request.form.get('request_id')
        
        if not all([tenant_id, apartment_id, request_id]):
            return "Missing required parameters", 400

        try:
            # Get tenant by ID
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return "Tenant not found", 404
                
            verify_tenant(landlord.id, tenant.id, int(apartment_id))
            delete_request(request_id)
            
            requests = VerificationRequest.query.filter_by(landlord_id=landlord.id).all()
            listings = ApartmentListing.query.filter_by(landlord_id=landlord.id).all()
            
            return render_template('landlordhome.html', requests=requests, listings=listings)
        except Exception as e:
            db.session.rollback()
            return str(e), 400
    
    return redirect(url_for('index_views.landlord_home'))  # Handle GET requests

       
@landlord_views.route('/landlord/decline_request',methods=['GET', 'POST'])
@jwt_required()
def decline_request():
    current_username = get_jwt_identity()
    landlord = Landlord.query.filter_by(username=current_username).first()
    request_id = request.form['request_id']
    requests = VerificationRequest.query.filter_by(landlord_id=landlord.id).all()
    delete_request(request_id)
    return render_template('landlordhome.html', listings=ApartmentListing.query.all(),requests = requests)

