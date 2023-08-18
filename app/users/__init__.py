from flask import Blueprint,url_for

#Define a Blueprint for user. Important to include static_url_path to avoid conflict with main app
user_bp = Blueprint('user',__name__,template_folder='templates',static_folder='static', static_url_path='/user/static')

#Import routes 
from . import routes
