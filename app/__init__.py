from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from .users import user
from .private import db
def create_app():
     app = Flask(__name__)
     '''app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
     app.config['UPLOAD_FOLDER'] = 'app/private/static/images'
     '''
     app.config.from_object("config.DevConfig")
     print(app.config['HOST'])
     #Import BluePrint for public part
     from .public import public_bp
     #Register BluePrint
     app.register_blueprint(public_bp)
     #Register user BLueprint
     from .users import user_bp
     app.register_blueprint(user_bp)
     #Register private BluePrint
     from .private import private_bp
     app.register_blueprint(private_bp)

     #Initialize LoginManager
     login_manager = LoginManager(app)

     #Indicate which is the login view
     login_manager.login_view = "user.do_login"
    
     @login_manager.user_loader
     def load_user(user_id):
        return   user.User.get_user(user_id)
     



     return app 