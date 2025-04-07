from flask import Blueprint

# Create the Blueprint for the 'auth' module
auth = Blueprint('auth', __name__)

# Import routes after creating the Blueprint to avoid circular imports
from . import routes