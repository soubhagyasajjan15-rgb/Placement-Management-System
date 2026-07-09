import mysql.connector

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root123",
        database="placement_db"
    )

    print("Connected Successfully!")
    connection.close()

except mysql.connector.Error as err:
    print("MySQL Error:", err)