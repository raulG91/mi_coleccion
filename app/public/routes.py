from flask import abort, render_template,request,redirect,url_for,current_app
from flask_login import current_user, login_required
from . import public_bp
from .forms import NewGameForm, GameDetailsForm, FIlterForm
from .model import Product,Game, Controller,Stats
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
import math
import json
from PIL import Image,ExifTags
from io import BytesIO
import pillow_heif



@public_bp.route('/')
def index():
    if  current_user.is_authenticated:
        return redirect(url_for('public.landpage'))  
    else:    
        return render_template('index.html')


@public_bp.route('/landpage',defaults={'page': None,}, methods=['GET','POST'])
@public_bp.route('/landpage/<int:page>',methods=['GET','POST'])
@login_required
def landpage(page:int):
    filter_form = FIlterForm()
    conditions = {}
    if request.method == 'POST':
        if request.form.get('newProduct'):
            #Redirec to new game action
            return redirect(url_for('public.new_game'))
        elif request.form.get("filter_button"):
            if filter_form.validate_on_submit:
                platform = filter_form.platform.data
                genre = filter_form.genre.data
                region = filter_form.region.data
                id_user =  current_user.get_id()
                #Set a dictionary with all conditions
                conditions['genre'] = genre
                conditions['region'] = region
                conditions['platform'] = platform
                items_page = current_app.config["ITEMS_PAGE"]  
                number_products = Controller.get_total_items(id_user=id_user,condition=conditions)
                pages = calculate_pages(number_products,items_page)
                filtered_products= Controller.get_games_for_user(id_user,0,items_page,condition=conditions)
                messages = []
                return render_template('landpage.html', form = filter_form, messages=messages, products = filtered_products,filter = json.dumps(conditions), current_page = 1, total_pages=pages,total_products = number_products)
        elif request.form.get("char"):
                return redirect(url_for("public.stadistics"))
        else: 
             return redirect(url_for('public.landpage'))    
    elif request.method == 'GET':
        filter_conditions = None
        filter = request.args.get("filter")
        if filter:
            filter_conditions = json.loads(filter)            
        id_user =  current_user.get_id()
        items_page = current_app.config["ITEMS_PAGE"] 
        number_products = Controller.get_total_items(id_user=id_user,condition=filter_conditions)
        pages = calculate_pages(number_products,items_page)
        if page:
            #Get limits for pagination
            lower_limit = items_page * (page-1)
        else:
            page = 1
            lower_limit = 0
         #Get Products 
        products= Controller.get_games_for_user(id_user,lower_limit,items_page,condition=filter_conditions)
        messages = []
        if filter_conditions:
            return render_template('landpage.html', form = filter_form, messages=messages, products = products,filter = json.dumps(filter_conditions),current_page = page, total_pages = pages, total_products = number_products)
        else:
             return render_template('landpage.html', form = filter_form, messages=messages, products = products,current_page = page, total_pages = pages,total_products = number_products)


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
            # Resize the image (you can change max_width and max_height)
            resized_image = resize_image(image, max_width=500, max_height=500) 
            # Define the full path to save the image
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename)

            # Save the resized image to disk
            with open(image_path, 'wb') as f:
                f.write(resized_image.read()) 
            
            #Store the image in the corresponding folder
            #image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename))
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

@public_bp.route('/filter', methods=['GET','POST'])
@login_required
def filter():
    form = FIlterForm()

    if form.validate_on_submit:
        print("Hola")

@public_bp.route('/stadistics',methods=['GET','POST'])
def stadistics():
    id_user =  current_user.get_id()
    total_items = Controller.get_total_items(id_user)
    stats = Stats()
    games_platform = stats.get_by_platform(id_user=id_user)
    print(games_platform)
    current_year = stats.get_producs_current_year(id_user)
    current_month = stats.get_products_current_month(id_user=id_user)
    total_price = stats.get_total_price(id_user=id_user)
    return render_template("stadistics.html", total_items = total_items,items_year = current_year, items_month = current_month,total_price = total_price,games_platform=games_platform)           
def calculate_pages(elements,items_page:int)->int:
    #Get configuration parameter 
    num_pages = math.ceil(elements/items_page)
    return num_pages

'''''
Functions to handle images
'''

# Register HEIC support once at the start of your application
pillow_heif.register_heif_opener()

# Function to determine the format of the image file
def get_image_format_by_extension(filename):
    ext = filename.lower().split('.')[-1]
    
    if ext == 'heic':
        return 'HEIC'
    elif ext in ['jpeg', 'jpg']:
        return 'JPEG'
    elif ext == 'png':
        return 'PNG'
    # Add other formats as needed
    else:
        return 'Unknown'

def detect_image_format(image_file):
    # Check MIME type if available
    if hasattr(image_file, 'content_type'):
        mime_type = image_file.content_type
        if mime_type == 'image/heic':
            return 'HEIC'
        elif mime_type == 'image/jpeg':
            return 'JPEG'
        elif mime_type == 'image/png':
            return 'PNG'
    
    # Fall back to checking file extension
    filename = image_file.filename
    return get_image_format_by_extension(filename)

# Resize function with format handling
def resize_image(image_file, max_width, max_height):
    # Detect format
    format_detected = detect_image_format(image_file)
    print(f"Detected format: {format_detected}")
    
    # Open and process the image
    img = Image.open(image_file)
    
    # Fix orientation
    img = fix_image_orientation(img)

    # Resize the image
    img.thumbnail((max_width, max_height))

    # Prepare to save in an appropriate format
    img_byte_arr = BytesIO()
    output_format = format_detected if format_detected != 'HEIC' else 'JPEG'
    print("Saving as format:", output_format)
    
    # Save the image to the byte array
    img.save(img_byte_arr, format=output_format, optimize=True, quality=85)
    img_byte_arr.seek(0)
    
    return img_byte_arr

# EXIF orientation handling function (same as before)
def fix_image_orientation(img):
    try:
        exif = img._getexif()
        if exif is not None:
            orientation = None
            for tag, value in ExifTags.TAGS.items():
                if value == 'Orientation':
                    orientation = tag
                    break
            if orientation and exif.get(orientation):
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
        return img
    except Exception as e:
        print(f"Error processing EXIF orientation: {e}")
        return img
