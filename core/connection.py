
import mysql.connector

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'peluqueriabd',
    'password': '123456',
'auth_plugin': 'mysql_native_password'
}

connection = mysql.connector.connect(**mysql_config)

def get_connection():
    return connection
