from flask import Flask
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        cnx = mysql.connector.connect(
            user='root', 
            password='root',
            host='bancodados',
            database='mydb'
        )
    except Error as e:
        print("Error while connecting to MySQL", e)
    

    return '<p> Hello world </p>'

if __name__ == '__main__':
    app.run(port=8080,debug=True,host='0.0.0.0')