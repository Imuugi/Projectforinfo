from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize,get_user_by_username

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
    return render_template('homepage.html')

@index_views.route('/landlordhome')
def landlord_home():
    return render_template('landlordhome.html')

@index_views.route('/landlord-login.html')  # Route to serve the landlord login page
def show_landlord_login():
    return render_template('landlord-login.html')
