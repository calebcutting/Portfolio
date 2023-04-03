import mysql.connector

db = mysql.connector.connect(host='localhost',
                             user='root',
                             passwd='root',
                             database='testdatabase')

mycursor = db.cursor()