class Config(object):
    SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    UPLOAD_FOLDER = "app/private/static/images"

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
    HOST = 'raulg91.mysql.pythonanywhere-services.com'
    USER = 'raulg91'
    PASSWORD = 'Database+2023'
    DATABASE = 'raulg91$mi_coleccion'