from flask import Flask, render_template, request, session, jsonify, redirect,url_for
from auth.routes import auth
from restaurants.routes import restaurants
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson import ObjectId
from auth.models import User
from datetime import timedelta

# Initialize the Flask app
app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'rs143lu@'  # Use a strong secret key
app.config['MONGO_URI'] = "mongodb://sunny:rs143lu%40@localhost:27017/MyDB"

# Initialize PyMongo
mongo = PyMongo(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(restaurants, url_prefix='/restaurants')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Define the index route
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading homepage: {e}", 500

@login_manager.user_loader
def load_user(user_id):
    try:
        user = mongo.db.FDUsers.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(user["_id"])
    except Exception as e:
        print(f"Error in load_user: {e}")
    return None

@app.route('/set_session')
def set_session():
    session.permanent = True  # Ensures the session uses PERMANENT_SESSION_LIFETIME
    session['user_id'] = 'example_user_id'
    session['cart'] = []  # Initialize the cart in the session
    return "Session set with a timeout of 10 minutes."

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        # Retrieve item data from the form
        item_name = request.form.get('name')
        item_price = float(request.form.get('price'))

        # Debug: Ensure form data is being received
        print(f"Item Name: {item_name}, Item Price: {item_price}")

        # Initialize the cart in the session if not present
        if 'cart' not in session:
            session['cart'] = []

        # Check if the item already exists in the cart
        cart = session['cart']
        existing_item = next((item for item in cart if item['name'] == item_name), None)

        if existing_item:
            existing_item['quantity'] += 1  # Increase the quantity
        else:
            cart.append({'name': item_name, 'price': item_price, 'quantity': 1})  # Add a new item

        # Save updated cart back to the session
        session['cart'] = cart

        # Debug: Print the updated cart
        print(f"Updated Cart: {session['cart']}")

        # Return the updated cart count as a JSON response
        total_items = sum(item['quantity'] for item in cart)
        return jsonify({'cart_count': total_items})

    except Exception as e:
        # Debug: Print the error for troubleshooting
        print(f"Error in /add_to_cart: {e}")
        return jsonify({'error': 'An error occurred while adding to cart'}), 500

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_items = sum(item['quantity'] for item in cart_items)
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_items=total_items, total_amount=total_amount)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    item_name = request.form.get('name')
    action = request.form.get('action')

    # Check if the cart exists in session
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']
    for item in cart:
        if item['name'] == item_name:
            if action == 'increase':
                item['quantity'] += 1
            elif action == 'decrease' and item['quantity'] > 1:
                item['quantity'] -= 1
            break

    session['cart'] = cart  # Save updated cart back to session
    return redirect(url_for('cart'))

if __name__ == "__main__":
    app.run(debug=True)
