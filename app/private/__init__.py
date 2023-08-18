from flask import Blueprint,url_for

#Define a Blueprint for public. Important to include static_url_path to avoid conflict with main app
private_bp = Blueprint('private',__name__,template_folder='templates',static_folder='static', static_url_path='/private/static')
