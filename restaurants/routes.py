from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from restaurants.models import fetch_all_restaurants, insert_restaurant, fetch_menu_by_restaurant_id

restaurants = Blueprint('restaurants', __name__)

@restaurants.route('/', methods=['GET'])
@login_required
def get_restaurants():
    restaurants = fetch_all_restaurants()
    if restaurants is not None:
        return render_template('restaurants.html', restaurants=restaurants)
    else:
        return jsonify({"error": "Could not fetch restaurants"}), 500

@restaurants.route('/restaurants', methods=['POST'])
def add_restaurant():
    data = request.get_json()
    if insert_restaurant(data):
        return jsonify({"message": "Restaurant added successfully!"}), 201
    else:
        return jsonify({"error": "Failed to add restaurant"}), 500

@restaurants.route('/menus/<restaurant_id>', methods=['GET'])
def get_menu(restaurant_id):
    restaurant = fetch_menu_by_restaurant_id(restaurant_id)

    if restaurant and "menu" in restaurant:
        return render_template('menu.html', menu=restaurant["menu"], restaurant_name=restaurant["name"])
    else:
        return jsonify({"error": "Menu not found for this restaurant"}), 404
