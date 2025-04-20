from flask import Blueprint, render_template, request
from App.controllers import (create_review,view_reviews)
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models import ApartmentListing
tenant_views = Blueprint('tenant_views',__name__,template_folder='../templates')

@tenant_views.route('/tenant/create_review',methods=['GET', 'POST'])
@jwt_required()
def create_review():
    tenant_id = get_jwt_identity()
    if request.method == 'POST':
        content = request.form['content']
        rating = request.form['rating']
        apartment_id = request.form['apartment_id']

        review = create_review(tenant_id,content,rating,apartment_id)
        return render_template('index.html')
    
    return render_template('index.html')

@tenant_views.route('/tenant/view_reviews',methods=['GET', 'POST'])
@jwt_required()
def view_reviews():
    tenant_id = get_jwt_identity()
    reviews = view_reviews(tenant_id)
    return render_template('index.html',reviews = reviews)

@tenant_views.route('/search')
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
    elif filter_by == 'price':
        try:
            price_value = float(query)
            results = ApartmentListing.query.filter(ApartmentListing.price <= price_value).all()
        except ValueError:
            results = []
    else:
        results = []

    return render_template('search_results.html', results=results, query=query, filter_by=filter_by)