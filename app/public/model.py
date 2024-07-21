from app.private.db import db_connection
import os
from flask import current_app
import json
from datetime import datetime
class Product:
    def __init__(self,name,description,buy_date,price):
        self._id_product = 0
        self.name = name
        self.description = description
        self.buy_date = buy_date
        self.price = price
    def get_product_id(self):
        return self._id_product
    def set_pruduct_id(self,id):
        self._id_product = id    
    def get_name(self):
        return self.name
    def set_name(self,name):
        self.name = name
    def get_description(self):
        return self.description
    def set_description(self,description):
        self.description = description
    def get_buy_date(self):
        return self.buy_date
    def set_buy_date(self,date):
        self.buy_date = date
    def get_price(self):
        return self.price
    def set_price(self,price):
        self.price = price     

class Game(Product):   
    def __init__(self):
        self.platform = ""
        self.genre = ""
        self.region = ""
        self.publisher = ""
        self.status = ""
        self.buyer_platform = ""
        self.image = ""
    def _list_to_object(self,list):
        self.set_pruduct_id(list[0])
        self.set_name(list[1])
        self.set_description(list[2])
        self.set_buy_date(list[3])
        self.set_price(list[4])
        self.set_platform(list[5])
        self.set_genre(list[6])
        self.set_region(list[7])
        self.set_publisher(list[8])
        self.set_status(list[9])
        self.set_buyer_platform(list[10])
        self.set_image(list[11])

    def get_platform(self):
        return self.platform
    def set_platform(self,platform):
        self.platform = platform
    def get_genre(self):
        return self.genre
    def set_genre(self, genre):
        self.genre = genre 
    def get_region(self):
        return self.region
    def set_region(self,region):
        self.region = region
    def get_publisher(self):
        return self.publisher
    def set_publisher(self,publisher):
        self.publisher = publisher
    def get_status(self):
        return self.status
    def set_status(self,status):
        self.status = status
    def get_buyer_platform(self):
        return self.buyer_platform
    def set_buyer_platform(self,buyer_platform):
        self.buyer_platform = buyer_platform
    def get_image(self):
        return self.image
    def set_image(self, image):
        self.image = image    
    def add_game(self,name,description,buy_date,price,platform,genre,region,publisher,status,buyer_platform,image,user_id):
        '''
        Add a new game into the db for an specific user
        :param name: Name for the product
        :param description: Description for the product
        :param buy_date: Date in format YYYY-MM-DD when product was bought
        :param price: Price in format NN.NN 
        :param platform : String that contains platform for the game
        :param genre: String with the genre for game
        :param region: String with the reegion for game
        :param publisher: String to identify the publisher for the game
        :param status: String to indicate the status of the game
        :param buyer_platform: String with the platform where the product was bought 
        :param user_id: Id of the user associated to the game
        :return : True if the game was added to the app False otherwise
        '''
        result = True
        #Create an object to handle database connection
        database = db_connection()
        self.name = name
        self.description = description
        self.buy_date = buy_date
        self.price = price 
        self.platform = platform
        self.genre = genre
        self.region = region
        self.publisher = publisher
        self.status = status
        self.buyer_platform = buyer_platform
        self.image = image
        
        #First create the product in table product
        insert_string = f'insert into product (name,description,buy_date,price,id_user_fk) values(\'{self.name}\',\'{self.description}\',\'{self.buy_date}\',{self.price},{user_id})'
        result_db = database.execute_insert(insert_string)

        if result_db:
            #Game has been inserted into product table, let's get the id generated
            for value in result_db:
                self.set_pruduct_id(value[0])
                print(str(self.get_product_id()))
            #Once the product has been inserted, we insert game details into table Game
            insert_string = f'insert into game values({self.get_product_id()},\'{self.platform}\',\'{self.genre}\',\'{self.region}\',\'{self.publisher}\',\'{self.status}\',\'{self.buyer_platform}\',\'{self.image}\')'    
            result_db = database.execute_insert(insert_string)
            if result_db:
                #Game has been created correctly
                result = True
            else:
                delete_string = f'delete from product where id_product = {self.get_product_id()}'
                database.execute_delete(delete_string)
                result = False    
        else:
            #There was an issue inserting the product into the database 
            result = False

        return result
    def get_game_id(self,id_game,id_user):
    
        database = db_connection()
        query_string = f'select p.id_product,p.name,p.description,p.buy_date,p.price,g.platform,g.genre,g.region,g.publisher,g.status,g.buyer_platform, g.image from product p inner join game g on p.id_product = g.id_product and p.id_product = {id_game} and id_user_fk = {id_user}'
        query_result  = database.execute_query(query_string)
        result = True
        if query_result:
            #First entry in the tuple contains value for specific game
            self._list_to_object(query_result[0])
        else:
            result = False
        return result        


    def delete_game(self):

        database = db_connection()
        delete_string = f'delete from product where id_product = {self._id_product}'
        result_deletion  =  database.execute_delete(delete_string)
        if result_deletion and self.image:
            #if information has been deleted from database, delete image store
            app_folder = current_app.config['UPLOAD_FOLDER']
            os.remove(f'{app_folder}/{self.image}')

        return result_deletion
    def modify_game(self,name_new,description_new,buy_date_new,price_new,platform_new,genre_new,region_new,publisher_new,status_new,buyer_platform_new):
        '''
        Modify a game
        :param name_new: New name for the product
        :param description_new: New Description for the product
        :param buy_date_new : New Date in format YYYY-MM-DD when product was boughtz
        :param price_new: New Price in format NN.NN 
        :param platform_new : String that contains platform for the game
        :param genre_new : String with the genre for game
        :param region_new : String with the reegion for game
        :param publisher_new: String to identify the publisher for the game
        :param status_new : String to indicate the status of the game
        :param buyer_platform_new : String with the platform where the product was bought 
        :return : True if the game was updated successfully False otherwise
        '''
        database = db_connection()
        update_string = f'update product set name = \'{name_new}\',description = \'{description_new}\', buy_date = \'{buy_date_new}\', price = {price_new} where id_product = {self._id_product}'
        result_update = database.execute_update(update_string)

        if result_update:
            #Update object properties with new values
            self.set_name(name_new)
            self.set_description(description_new)
            self.set_buy_date(buy_date_new)
            self.set_price(price_new)
            update_string = f'update game set platform = \'{platform_new}\', genre = \'{genre_new}\', region = \'{region_new}\', publisher = \'{publisher_new}\', status = \'{status_new}\', buyer_platform = \'{buyer_platform_new}\'  where id_product = {self._id_product}'       
            result_update = database.execute_update(update_string)

            if result_update:
                #Update object with new values
                self.platform = platform_new
                self.genre = genre_new
                self.region = region_new
                self.publisher = publisher_new
                self.status = status_new
                self.buyer_platform = buyer_platform_new
            return result_update
        else:
            return result_update       
class Controller:
    @classmethod
    def get_games_for_user(self,id_user,min:int,offset:int,condition:dict = None):
        games = []
        if condition:
            condition_string = ""
            for key in condition:
                if condition[key]:
                    condition_string+=f' and {key} = \'{condition[key]}\''
            query_string = f'select p.id_product,p.name,p.description,p.buy_date,p.price,g.platform,g.genre,g.region,g.publisher,g.status,g.buyer_platform, g.image from product p inner join game g on p.id_product = g.id_product {condition_string} and p.id_user_fk = {id_user} LIMIT {min},{offset}'
        
        else:
            query_string = f'select p.id_product,p.name,p.description,p.buy_date,p.price,g.platform,g.genre,g.region,g.publisher,g.status,g.buyer_platform, g.image from product p inner join game g on p.id_product = g.id_product and p.id_user_fk = {id_user} LIMIT {min},{offset}'
        database = db_connection()
        query_result = database.execute_query(query_string)
        if query_result:
          
            for value in query_result:
                new_game = Game()
                new_game.set_pruduct_id(value[0])
                new_game.set_name(value[1])
                new_game.set_description(value[2])
                new_game.set_buy_date(value[3])
                new_game.set_price(value[4])
                new_game.set_platform(value[5])
                new_game.set_genre(value[6])
                new_game.set_region(value[7])
                new_game.set_publisher(value[8])
                new_game.set_status(value[9])
                new_game.set_buyer_platform(value[10])
                new_game.set_image(value[11])
                games.append(new_game)
        return games    
    @classmethod
    def get_total_items(self,id_user,condition:dict=None):
        '''
        Get number of products for user with or without condition
        '''
        if condition:
            condition_string = ""
            for key in condition:
                if condition[key]:
                    condition_string+=f' and {key} = \'{condition[key]}\''
            query_string = f'select count(*) as total from product p join game g on p.id_product = g.id_product and p.id_user_fk = {id_user} {condition_string}'
        else:
            query_string = f'select count(*) as total from product where id_user_fk = {id_user}'    
        database = db_connection()
        query_result = database.execute_query(query_string=query_string)
        number_products = 0
        if query_result:
            number_products = query_result[0][0]
        return number_products    
class Stats:

    def __init__(self):
        pass    
    
    def get_by_platform(self,id_user)->list:
        '''
        Get number of games by platform 
        :param id_user: User id
        :return: JSON String, array with many objects as games by platform. Object returned will have 2 keys: platform and number
        '''

        #Create query string 
        query_string = f'SELECT count(platform),platform FROM game g INNER join product p on g.id_product = p.id_product and p.id_user_fk = {id_user} GROUP by platform;'
        database = db_connection()
        query_result = database.execute_query(query_string=query_string)
        result = []
        for value in query_result:
            object = {
                "platform":value[1],
                "number":value[0]
            }
            result.append(object)
        result_dict = {
            "elements": result
        }
        return json.dumps(result_dict)    
    
    def get_total_price(self,id_user):

        query_string = f'SELECT sum(price) FROM product WHERE id_user_fk = \'{id_user}\';'
        database = db_connection()
        query_result = database.execute_query(query_string=query_string)
        total = 0
        for value in query_result:
            if value[0]:
                total = value[0]
            else:
                total = 0    
        return total    

    
    def get_producs_current_year(self,id_user)->int:
        '''
        Return number of products bought during this year
        :param id_user: User id to check
        :return Number of products bought during this year
        '''
        today = datetime.now().strftime("%Y-%m-%d")
        begin_year = datetime(datetime.now().year,1,1).strftime("%Y-%m-%d")
        query_string = f'SELECT count(*) FROM product where buy_date BETWEEN \'{begin_year}\' and \'{today}\' and id_user_fk = {id_user} ;'
        database = db_connection()
        query_result = database.execute_query(query_string=query_string)
        num_products = 0
        for value in query_result:
            num_products = value[0]
        return num_products
    def get_products_current_month(self,id_user):
        '''
        Return number of products bought during this month
        :param id_user: User id to check
        :return Number of products bought during this month
        '''        
        today = datetime.now().strftime("%Y-%m-%d")
        begin_month = datetime(datetime.now().year,datetime.now().month,1).strftime("%Y-%m-%d")
        query_string = f'SELECT count(*) FROM product where buy_date BETWEEN \'{begin_month}\' and \'{today}\' and id_user_fk = {id_user} ;'
        database = db_connection()
        query_result = database.execute_query(query_string=query_string)
        num_products = 0
        for value in query_result:
            num_products = value[0]
        return num_products