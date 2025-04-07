from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from auth.models import register_user, authenticate_user
from flask_login import login_user,logout_user
from auth.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            # Handle JSON-based requests
            data = request.get_json()
        else:
            # Handle form-based requests
            data = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'password': request.form.get('password')
            }

        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields"}), 400

        # Process registration
        user = register_user(data['name'], data['email'], data['password'])
        if 'error' in user:
            if request.is_json:
                return jsonify(user), 400
            else:
                # Render the form with an error message
                return render_template('register.html', error=user['error'])

        # Success response
        if request.is_json:
            return jsonify({"message": "User registered successfully", "redirect_url": url_for('restaurants.get_restaurants')}), 201
        else:
            # Redirect after successful registration (for form-based requests)
            return redirect(url_for('restaurants.get_restaurants'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = authenticate_user(username, password)
        if user:
            login_user(User(user["_id"]))  # Log the user in
            # Directly redirect to the restaurants page
            return redirect(url_for('restaurants.get_restaurants'))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)

    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()  # Logs the user out
    return redirect(url_for('index')) 