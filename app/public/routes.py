

from flask import abort, render_template,request,redirect,url_for,current_app
from flask_login import current_user, login_required
from . import public_bp
from .forms import NewGameForm, GameDetailsForm
from .model import Product,Game, Controller
from werkzeug.utils import secure_filename
import os
from uuid import uuid4


@public_bp.route('/')
def index():
    if  current_user.is_authenticated:
        return redirect(url_for('public.landpage'))  
    else:    
        return render_template('index.html')

@public_bp.route('/landpage', methods=['GET','POST'])
@login_required
def landpage():
    if request.method == 'POST':
        if request.form.get('newProduct'):
            #Redirec to new game action
            return redirect(url_for('public.new_game'))
        else: 
             return redirect(url_for('public.landpage'))    
    elif request.method == 'GET':
        #if there is a get request render template landpage

        #Get Products 
        id_user =  current_user.get_id()
        products = Controller.get_games_for_user(id_user)
        messages = []
        return render_template('landpage.html', messages=messages, products = products)

@public_bp.route('/new_game', methods=['GET','POST'])
@login_required
def new_game():
    form = NewGameForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        buy_date = form.buy_date.data
        price = form.price.data
        platform = form.platform.data
        genre = form.genre.data
        region = form.region.data
        publisher = form.publisher.data
        status = form.status.data
        buyer_platform = form.buyer_platform.data
        
        #Process image file, name of the element  FileField is upload-image
        image = request.files['upload-image']
        #Get image field name
        img_filename = secure_filename(image.filename)
         
        if img_filename:
             # Make file name unique
            ident = uuid4().__str__()
            img_filename = f"{ident}-{img_filename}"
            #Store the image in the corresponding folder
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename))
        new_game = Game()
        id_user =  current_user.get_id()
        result = new_game.add_game(name,description,buy_date,price,platform,genre,region,publisher,status,buyer_platform,img_filename,id_user)

        if result:
            #After create game redirect to landpage
            return redirect(url_for('public.landpage'))
        else:
            #There was an issue creating the product
            form.form_errors = ["No se ha podido crear el producto, por favor intentelo de nuevo"]
            return render_template("new_game_form.html", form=form)
    else:        
        return render_template("new_game_form.html", form=form)

    
@public_bp.route('/product/<int:product_id>', methods=['GET','POST'])
@login_required
def product_details(product_id:int):
    form = GameDetailsForm()
    messages = []
    game = Game()
    game.set_pruduct_id(product_id)
    if request.method == 'GET':
        #If there is a get request, set values for game id in the form
      
        exist =  game.get_game_id(product_id,current_user.get_id())

        if exist :

            #Fill the form with the data from Database 
            form.name.data = game.get_name()
            form.description.data = game.get_description()
            form.buy_date.data = game.get_buy_date()
            form.price.data = game.get_price()
            form.platform.data = game.get_platform()
            form.genre.data = game.get_genre()
            form.region.data = game.get_region()
            form.publisher.data = game.get_publisher()
            form.status.data = game.get_status()
            form.buyer_platform.data = game.get_buyer_platform()
            images = game.get_image()   
            return render_template("game_details.html",form = form, messages = messages, images = images)
        else:
            #Product doesn't belong to login employee
            return redirect(url_for('public.landpage'))
    else:
        #if it is a post method, check the button first
        if request.form.get('modify'):

            if form.validate_on_submit():
                name_new = form.name.data
                description_new = form.description.data
                buy_date_new = form.buy_date.data
                price_new = form.price.data
                platform_new = form.platform.data
                genre_new = form.genre.data
                region_new = form.region.data
                publisher_new = form.publisher.data
                status_new = form.status.data
                buyer_platform_new = form.buyer_platform.data
                result = game.modify_game(name_new,description_new,buy_date_new,price_new,platform_new,genre_new,region_new,publisher_new,status_new,buyer_platform_new)
                if result:
                    #After modify game redirect to landpage
                    return redirect(url_for('public.landpage'))
                else:
                    messages = ["se ha producido un error durante la actulizacion"]
                    #Update form values just in case some values were updated
                    exist = game.get_game_id(product_id,current_user.get_id())

                    if  exist :

                        form.name.data = game.get_name()
                        form.description.data = game.get_description()
                        form.buy_date.data = game.get_buy_date()
                        form.price.data = game.get_price()
                        form.platform.data = game.get_platform()
                        form.platform.data = game.get_platform()
                        form.genre.data = game.get_genre()
                        form.region.data = game.get_region()
                        form.publisher.data = game.get_publisher()
                        form.status.data = game.get_status()
                        form.buyer_platform.data = game.get_buyer_platform()
                        images = game.get_image()
                        return render_template("game_details.html",form = form, messages = messages, images = images )                    
                    else:
                        #Product doesn't belong to login employee
                        return redirect(url_for('public.landpage'))            
            else:  
                #Not validate form yet
                images = game.get_image()
                return render_template("game_details.html",form = form, messages = messages, images = images )  
        else:
            #User has pressed button delete
            #Get details for the game
            game.get_game_id(product_id,current_user.get_id())

            if game.delete_game():
        
                #if the information has be deleted succesfully retrun to landpage
                return redirect(url_for('public.landpage'))
            else:
                #if there was an issue deleting the product indicate it
                messages = ["Se ha producido durante el borrado"]
                images = game.get_image()
                return render_template("game_details.html",form = form, messages = messages, images = images)    

           
        