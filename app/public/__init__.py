from flask import Blueprint,url_for

#Define a Blueprint for public. Important to include static_url_path to avoid conflict with main app
public_bp = Blueprint('public',__name__,template_folder='templates',static_folder='static', static_url_path='/public/static')

#Import routes 
from . import routes
