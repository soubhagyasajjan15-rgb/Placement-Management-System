import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # Your MySQL username
            password="root123",   # Replace with your actual MySQL password
            database="placement_db"
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database Connection Error:", e)
        return None