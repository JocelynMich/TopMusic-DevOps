#CODIGO PARA LA CREACION DE LA BASE DE DATOS
import mysql.connector

#Creando un conector
mydb=mysql.connector.Connect(
    host='localhost',
    user='root',
    password='K1m_D0kja20KAJ2M',
)

cursor= mydb.cursor()
cursor.execute('USE MUSIC')
cursor.execute('CREATE TABLE Billboard(ranking INT(15), song VARCHAR(150), artist VARCHAR(150), image_url VARCHAR(200))')
cursor.close()