# App Details

The aim of this app is to store all information about your video games. It is a web application that will allow you to access online to all information about your games. Application could be used from a mobile device or PC.

Users could create an account to start using app functionalities. Once user is logged into the application it could add items and for each item user could add all relevant information. User can also manage all games stored in the database (update and delete).

This application has been deployed into Pythonanywhere.

# Main functionalities

- Create user account
- Manage user profile
- Delete user account
- Add video games
- Update/delete item
- Filter items
- Get stadistics 

# Technology

- **Frontend**: It is doveloped using HTML, CSS and Javascript
- **Backend**: It is a flask app application so all functionalities are developed using python.
- **Database**: Databse used by the application is a Mysql database.

# Installation

1. Install `requirements.txt` file in a virtual environment
2. Use file `databse.sql` to create needed tables and to have some examples.
3. Create  `config.py` with needed details. It contains 2 clases, one is used for local development and the other for production. Create a new SECRET_KEY to be used in your app.
   As example:
   ``` 
   class Config(object):
    SECRET_KEY = ''
    UPLOAD_FOLDER = "/private/static/images"
    ITEMS_PAGE = 30 #Items per page for pagination

    class DevConfig(Config):
        DEBUG = True
        TESTING = True    
        HOST = 'localhost'
        USER = 'root'
        PASSWORD = ''
        DATABASE = 'mi_coleccion'
    class ProdConfig(Config):
        DEBUG = False
        TESTING = False      
    ```

# Roadmap

- Allow to update multiple images for each game
- Add extra information about a game, for example if you have play it. 

