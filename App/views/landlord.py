from App.models import Landlord
from flask import Blueprint, render_template
from App.controllers import (view_listings, create_listing, verify_tenant)


landlord = Blueprint('landlord',__name__,template_folder='templates')

@view_listings
@landlord.route('/view_aparetments')
def list_apartments(landlord_id):
    listings = view_listings(landlord_id)
    return render_template('index.html',listings = listings)



@create_listing
@landlord.route('/create_review')
def create_review(landlord_id):
   

   
