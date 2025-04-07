import logging
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask import jsonify
from flask_login import UserMixin

client = MongoClient("mongodb://sunny:rs143lu%40@localhost:27017/MyDB") 
db = client['MyDB'] 
users_collection = db['FDUsers']

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)

# Password hashing
bcrypt = Bcrypt()

def register_user(name, email, password):
    try:
        print("Registering user:", name, email)
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            print("Email already exists:", email)
            return {"error": "Email already exists!"}

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = {"name": name, "email": email, "password": hashed_password}
        users_collection.insert_one(user)
        print("User registered successfully:", user)
        return {"message": "User registered successfully!", "user": {"name": name, "email": email}}
    except Exception as e:
        print("Error during registration:", str(e))
        return {"error": str(e)}


def authenticate_user(UserName, password):
    try:
        # Find the user by username
        user = users_collection.find_one({"name": UserName})
        if user:
            # Check if the provided password matches the stored hash
            if bcrypt.check_password_hash(user['password'], password):
                return user  # Return the full user object, including `_id`
            else:
                return None  # Invalid password
        else:
            return None  # User not found
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        return None


