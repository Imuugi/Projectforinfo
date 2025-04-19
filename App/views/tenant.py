from flask import Blueprint, render_template
from App.controllers import (create_review,view_reviews)
from flask_jwt_extended import jwt_required, get_jwt_identity

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
