import  pymysql
from flask import current_app

class db_connection:
    def __init__(self,database='mi_coleccion'):
        self.host = current_app.config['HOST']
        self.user = current_app.config['USER']
        self.password = current_app.config['PASSWORD']
        self.db = current_app.config['DATABASE']

        ''' 
        self.host ='localhost'
        self.user ='root'
        self.password = ''
        self.db = database 
        '''

    def _get_connection(self):
        self.connection = pymysql.connect( host=self.host,
                                user=self.user,
                                password= self.password,
                                db= self.db
                                )    
    def execute_query(self,query_string):
        self._get_connection()
        result = []
        with self.connection.cursor() as cursor:
            cursor.execute(query_string)
            result =  cursor.fetchall()
        self.connection.close()   
        return result
    def execute_insert(self, insert_string):
        self._get_connection()
        result = []
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_string)
                #Query to get last id inserted
                cursor.execute("Select last_insert_id()");    
                result = cursor.fetchall()
        except:
            self.connection.rollback()
            self.connection.close()
        else:    
            self.connection.commit()
            self.connection.close()    
        return result 
    def execute_delete(self, delete_string):
        self._get_connection()
        result = True

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(delete_string)
        except:
            self.connection.rollback()
            self.connection.close()
            result = False
        else:
            self.connection.commit()
            self.connection.close()
        return result                   
    def execute_update(self,update_string):

        self._get_connection()
        result = True

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(update_string)
        except:
            self.connection.rollback()
            self.connection.close()
            result = False
        else:
            self.connection.commit()
            self.connection.close()
        return result 
 