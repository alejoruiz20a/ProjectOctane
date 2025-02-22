import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import sqlite3
import json
from db.db import get_connection, release_connection

QUERIES_PATH = "json/queries.json"

# ENV
load_dotenv()
TOKEN = os.getenv("TOKEN")

with open(QUERIES_PATH,'r', encoding='utf-8') as file:
    queries = json.load(file)

# INTENTS
intents = discord.Intents.default()
intents.message_content = True  # Permite leer mensajes en servidores

# CLIENTE
bot = commands.Bot(command_prefix = "!", intents = intents)
#FDFSDFSDFSDF


@bot.command()
async def register(ctx):
    """Register yourself for the first time."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        id = str(ctx.author.id)
        username = ctx.author.name

        cursor.execute(queries['getUserById'],(id,))
        user = cursor.fetchone()

        if user:
            await ctx.send(f"Hello {user[1]}, you are already registered, you have ${user[2]}")
        else:
            cursor.execute(queries['insertUser'],(id,username))
            conn.commit()
            await ctx.send(f"Hello {username}, you have been succesfully registered.")
    except Exception as e:
        await ctx.send("Lo sentimos, ha habido un error, intentalo de nuevo más tarde.")

    finally:
        if conn:
            release_connection(conn)

@bot.command()
async def car_store(ctx):
    """See the car store where you can buy cars."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(queries["listCarModels"])
        cursor.fetchall()
        await ctx.send("Por el momento la tienda de autos no está disponible :(") 
        # AQUÍ VOY, DEBO DE APRENDER A LISTAR LOS CARROS DISPONIBLES PARA COMPRAR. 

    except Exception as e: 
        await ctx.send("Lo sentimos, ha habido un error, intentalo de nuevo más tarde.")

@bot.command()
async def buy(ctx, *car_name):
    if not car_name:
        await ctx.send("You have to type !buy [brand] [name] [year]")
        return

    await ctx.send(f"Searching for the {" ".join(car_name)}...")

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(queries["getCarModelByName"],(car_name[0], car_name[1], car_name[2]))
        car_model = cursor.fetchone()
        
        await ctx.send(f"Buying the {type(car_model)}")
    except Exception as e:
        await ctx.send(f"An error has ocurred... {e}")





# Iniciar el bot
bot.run(TOKEN)
