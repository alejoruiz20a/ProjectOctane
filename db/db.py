import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "car_game")
DB_USER = os.getenv("DB_USER", "bot_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "superseguro123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
MIN_CONN = 1
MAX_CONN = 5

import psycopg2
from psycopg2 import pool

try:
    connection_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=MIN_CONN,
        maxconn=MAX_CONN,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    if connection_pool:
        print("✅ Pool de conexiones creado exitosamente.")

except Exception as e:
    print(f"❌ Error al crear el pool de conexiones: {e}")
    connection_pool = None

def get_connection():
    if connection_pool:
        return connection_pool.getconn()
    else:
        raise Exception("⚠️ No hay pool de conexiones disponible.")

def release_connection(conn):
    if connection_pool:
        connection_pool.putconn(conn)

def close_pool():
    if connection_pool:
        connection_pool.closeall()
        print("🛑 Pool de conexiones cerrado.")
