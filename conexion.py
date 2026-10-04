import psycopg2


def obtener_conexion():
    conexion = psycopg2.connect(
        host="localhost",
        database="proyecto_integrador",
        user="postgres",
        password="adan2026",
        port="5432"
    )

    return conexion