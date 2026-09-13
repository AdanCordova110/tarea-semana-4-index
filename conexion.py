import mysql.connector


def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="adan2026",
        database="proyecto_integrador",
        port=3306
    )

    return conexion