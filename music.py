import discord
import yt_dlp
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"conectando a {channel.name}")
    else:
        await ctx.send("Debes estar en un canal de voz para usar este comando")

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.voice_client:
        await ctx.invoke(join)

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download = False)
        if 'entries' in info and info['entries']:  
            url = info['entries'][0]['url']
        else:
            await ctx.send("No se encontró la canción")
            return
    
    vc = ctx.voice_client
    vc.stop
    FFMPEG_OPTIONS = {'options': '-vn'}
    source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
    vc.play(source)

    await ctx.send(f"Reproduciendo: **{search}**")


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Desconectado del canal de voz.")
    else:
        await ctx.send("No estoy en un canal de voz.")

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}")

bot.run(TOKEN)





