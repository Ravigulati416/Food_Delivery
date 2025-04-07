from pymongo import MongoClient
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.ERROR)

# MongoDB Connection
client = MongoClient("mongodb://sunny:rs143lu%40@localhost:27017/MyDB")  # Update the URI if authentication is needed
db = client['MyDB']
restaurants_collection = db['FDRestaurants']  # Specify the collection for restaurants

# Fetch all restaurants
def fetch_all_restaurants():
    try:
        restaurants = list(restaurants_collection.find({}))
        return restaurants
    except Exception as e:
        logging.error(f"Error fetching all restaurants: {e}")
        return None

# Add a new restaurant
def insert_restaurant(data):
    try:
        restaurants_collection.insert_one(data)
        return True
    except Exception as e:
        logging.error(f"Error adding restaurant: {e}")
        return False

# Fetch menu of a specific restaurant
def fetch_menu_by_restaurant_id(restaurant_id):
    try:
        restaurant = restaurants_collection.find_one({"_id": restaurant_id})
        return restaurant
    except Exception as e:
        logging.error(f"Error fetching menu: {e}")
        return None
