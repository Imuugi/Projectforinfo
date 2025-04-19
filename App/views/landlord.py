from App.models import Landlord
from flask import Blueprint, render_template
from App.controllers import (view_listings, create_listing, verify_tenant,delete_apartment)


landlord = Blueprint('landlord',__name__,template_folder='templates')

@landlord.route('/view_apartments')
def list_apartments():
    landlord_id = get_jwt_identity()
    listings = view_listings(landlord_id)
    return render_template('index.html',listingsm  = listings)




@landlord.route('/landlord/create-listing', methods=['GET', 'POST'])
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


@landlord.route('/landlord/delete-listing',methods = ['GET','POST'])
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

@landlord.route('/landlord/verifytenant', methods = ['GET','POST'])
@jwt_required()
def verify_tenant():
    if request.method == 'POST':
        landlord_id = get_jwt_identity()
        tenant_id = request.form.get('tenant_id')
        verify_tenant(landlord_id,tenant_id)
        return "Tenant verified", 200

    return render_template('index.html')

