import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import sqlite3
import json
from db import connect_db

QUERIES_PATH = "json/queries.json"

# ENV
load_dotenv()
TOKEN = os.getenv("TOKEN")

with open(QUERIES_PATH,'r', encoding='utf-8') as file:
    queries = json.load(file)

# DB
conn = connect_db()
cursor = conn.cursor()

# INTENTS
intents = discord.Intents.default()
intents.message_content = True  # Permite leer mensajes en servidores

# CLIENTE
bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.command()
async def register(ctx):
    id = str(ctx.author.id)
    username = ctx.author.name

    cursor.execute(queries['getUserById'],(id,))
    user = cursor.fetchone()

    if user:
        await ctx.send(f"Hola {user[1]}, ya estás registrado como corredor, tienes ${user[2]}")
    else:
        cursor.execute(queries['insertUser'],(id,username))
        conn.commit()
        await ctx.send(f"Hola {username}, te has registrado como corredor.")

# Iniciar el bot
bot.run(TOKEN)
