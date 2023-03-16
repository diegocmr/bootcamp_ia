import mysql.connector
from CatchError import CatchError
from mysql.connector import Error
class Connection:
    def __init__(self,database="bancodados",autocommit=False):
        try:
            self.cnx = mysql.connector.connect(
                user='root', 
                password='root',
                host='bancodados',
                database='mydb',
                autocommit=autocommit
            )
        except Error as e:
            CatchError(e)
    def execute (self,sql,params,prepared=True):
        try:
            self.mycursor = self.cnx.cursor(prepared=prepared)
            self.mycursor.execute(sql, params)    
            return self.mycursor
        except Error as e:
            CatchError(e)
    def commit (self):
        try:
            self.cnx.commit()
        except Error as e:
            CatchError(e)    