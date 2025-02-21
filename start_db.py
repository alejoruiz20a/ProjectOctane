import psycopg2
import os
from dotenv import load_dotenv
from db.db import get_connection, release_connection
import json

load_dotenv()

MIGRATIONS_PATH = "db/migrations.sql"
CARS_PATH= "json/car_models.json"
QUERIES_PATH = "json/queries.json"

def insert_cars():
    try:
        conn = get_connection()
        cur = conn.cursor()

        with open(CARS_PATH, "r", encoding="utf-8") as file:
            car_models = json.load(file)

        with open(QUERIES_PATH,"r", encoding="utf-8") as file:
            queries = json.load(file)
        
        for car in car_models:
            cur.execute(queries['insertCarModel'],(car["brand"], car["model"], car["yr"], car["hp"], car["nm"], car["acc"],car["maxSpeed"], car["weight"], car["traction"], car["price"]))

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            release_connection(conn)

def run_migrations():
    try:
        conn = get_connection()
        cur = conn.cursor()

        with open(MIGRATIONS_PATH, "r", encoding="utf-8") as file:
            sql = file.read()
            cur.execute(sql)
        
        conn.commit()
        insert_cars()
        print("Migraciones ejecutadas correctamente.")
    except Exception as e:
        print(f"Error ejecutando las migraciones: {e}")
    finally:
        if conn:
            release_connection(conn)

    

run_migrations()