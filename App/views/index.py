from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize,get_user_by_username
from App.models import ApartmentListing

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/homepage', methods=['GET'])
def get_home_page():
    all_apartments = ApartmentListing.query.all()
    return render_template('homepage.html', listings=all_apartments)



@index_views.route('/landlordhome')
def landlord_home():
    all_apartments = ApartmentListing.query.all()
    return render_template('landlordhome.html', listings=all_apartments)

@index_views.route('/landlord-login.html') 
def show_landlord_login():
    return render_template('landlord-login.html')
    
@index_views.route('/login.html') 
def show_login():
    return render_template('login.html', methods=['GET'])

@index_views.route('/apartment/<int:apartment_id>')
def apartment_page(apartment_id):
    apartment = ApartmentListing.query.get_or_404(apartment_id)
    return render_template('apartmentpage.html', apartment=apartment)
