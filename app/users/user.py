from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..private import db


#Class User will enherid from UserMixin
class User(UserMixin):

    def __init__(self):
        self.id = 0
        self.name =""
        self.last_name = "" 
        self.second_last_name = "" 
        self.email =  ""
        self.password =""
        self.isActive = True
        self.isAdmin = False
        self.db = db.db_connection()
    def set_password(self, password):
        self._password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def get_name(self):
        return self.name
    def get_last_name(self):
        return self.last_name
    def get_second_last_name(self):
        return self.second_last_name
    def get_email(self):
        return self.email
    def register_user(self,name,last_name,second_last_name, email, password, isActive=True, isAdmin=False):
        """
        Register an user into the application
        :return : 0 - User has been created, 1 - User already exist, 2 - error creating user
        """
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.isActive = isActive
        self.isAdmin = isAdmin
        return_value = 0
        #Before register user it is needed to check if the user already exists
        if not(self._exist_user()):
            #User doesn't exist, let's create it
            if self._save_user():
                return_value = 0
            else:
                return_value = 2

        else:
            return_value = 1

        return return_value



    def _exist_user(self):
        """
        Check if there is a user in the database with same email. 
        :return: True if user exist otherwise False
        """
        query_string = f'select * from users where email = \'{self.email}\' and is_active = \'1\';'
        result = self.db.execute_query(query_string)
        #if result list is empty there is not user with that email
        if not(result):
            return False 
        else:
            return True

    
    def _save_user(self):
        """
        Store user object into the database
        """
        user_created = False
        insert_string = f'insert into users (name,last_name,second_last_name,email,password,is_active,is_admin) values(\'{self.name}\',\'{self.last_name}\',\'{self.second_last_name}\',\'{self.email}\',\'{self.password}\',1,0)'
        self.db.execute_insert(insert_string)
        query_string = f'select id from users where email = \'{self.email}\' and is_active = \'1\';'
        query_result = self.db.execute_query(query_string)
        if query_result:
            for value in query_result:
                self.id = value[0]
                user_created = True
                break
        return user_created
    def _update_user(self):
        '''Update an user into the database'''
        
        update_string = f'update users SET name = \'{self.name}\', last_name = \'{self.last_name}\', second_last_name = \'{self.second_last_name}\', email = \'{self.email}\', password = \'{self.password}\' where id =\'{self.id} \';'
        user_updated = self.db.execute_update(update_string)
        return user_updated
    def _delete_user(self):
        '''Inactivate user in the DB'''
        delete_string = f'update users set is_active =\'0\' where id =\'{self.id} \';'
        user_updated = self.db.execute_update(delete_string)
        return user_updated       
    def _list_to_object(self,tuple):
        '''
        Get object attributes from a tuple from select query
        :param tuple: Tuple retruned from select statement
        '''
        self.id = tuple[0]
        self.name = str(tuple[1])
        self.last_name = str(tuple[2])
        self.second_last_name = str(tuple[3])
        self.email = str(tuple[4])
        self.password = str(tuple[5])
        if tuple[6] == 1: 
            self.isActive = True
        else: 
           self.isActive = False
        if tuple[7]:
            self.isAdmin = True
        else:
            self.isAdmin = False   

    def get_user_by_id(self,id):
        '''
        Get user  by id, check if the user exists in the database and get all information
        :param id: Id for the user
        :return True if the user exists otherwise it returns False
        '''
        query_string = f'select * from users where id = {id}'
        query_result = self.db.execute_query(query_string)
        user_exist = True

        if query_result:
            #Iterate over the list with results
            for value in query_result:
                self._list_to_object(value)
        else:
            user_exist = False
        return user_exist    
    def login_user(self,email,password):
        '''
        Check if email and password is associated to any user
        :param email: User's email
        :param password : User's password
        :return: True if user exists and False otherwise
        '''
        query_string = f'select * from users where email = \'{email}\' and is_active = 1'
        query_result = self.db.execute_query(query_string)
        user_exist = True

        if query_result:
            #if  user is in the database
            for value in query_result:
                self._list_to_object(value)
                #After read values store in the database check is password hash store 
                #match with the given password
                print(self.password)
                print(password)
                if self.check_password(password):
                    user_exist = True
                else:
                    user_exist = False    
        else:
            # No information was found in the databse therefore the user doesn't exist 
            user_exist = False
        return user_exist
    def update_user(self,name,last_name,second_last_name,email,password):
        '''
        Update user attributes
        '''
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name
        self.email = email
        self.password = generate_password_hash(password)
        result = self._update_user()
        return result
    def delete_user(self):
        '''Delete user'''
        result = self._delete_user()
        return result

    @staticmethod
    def get_user(id):
        user = User()
        if user.get_user_by_id(id):
            return user
        else:
            return None 