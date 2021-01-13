# bot.py
import os
import random
import datetime
from datetime import timedelta
import discord
from discord.ext import commands
import wolframalpha
import sqlite3
import csv
from gtts import gTTS
import asyncio
import pokepy
import numpy as np
import Responses
import userinfo
import sqlcrap
import info
from discord.errors import ClientException

TOKEN = open("Discord_Token.txt").read()
WOLFRAM_KEY = open('Wolfram_Key.txt').read()
intents = discord.Intents.default()
intents.members = True
client = wolframalpha.Client(WOLFRAM_KEY)
bot = commands.Bot(command_prefix="%", intents=intents)
pokeclient = pokepy.V2Client()


connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_number (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS bot_uses (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_message (name TEXT PRIMARY KEY, message TEXT)")
connection.commit()

board = np.arange(42).reshape(6, 7)

#on ready
@bot.event
async def on_ready():
    for guild in bot.guilds: 
        print("Connected to " + guild.name)

bot.add_cog(Responses.Responses(bot))
bot.add_cog(userinfo.User(bot))
bot.add_cog(sqlcrap.SQLCrap(bot))
bot.add_cog(info.Information(bot))

@bot.command(help = "disconnects the bot from whatever channel it is in")
async def leave(ctx):
    for client in bot.voice_clients:
        if client.guild == ctx.guild:
            await client.disconnect()

@bot.command(help = "Joins the voice channel you are currently in. Does not play anything", aliases = ["join"])
async def connect(ctx):
    try: 
        channelname = ctx.author.voice.channel
        await channelname.connect()
    except AttributeError:
        await ctx.send("You don't appear to be in a voice channel!")
    except ClientException:
        await ctx.send("I'm already in a voice channel!")
        

@bot.command(help = "Reads your message in the voice channel you are currently in")
async def read(ctx, *, arg):
    if (str(type(ctx.author.voice))) == "<class 'NoneType'>":
        await ctx.send("Not connected to a channel!")
    else:
        await ctx.send("Sorry, I haven't made this command yet")
 
@bot.command (help="Testing a voice command")
async def voicetest(ctx):
    channelname = ctx.author.voice.channel
    try:
        await channelname.connect()
    except(AttributeError, ClientException):
        pass
    resultant = discord.FFmpegPCMAudio(source="audiofilev2.wav", executable="/usr/bin/ffmpeg")
    ctx.voice_client.play(resultant)
    await ctx.send("This is not a finished command yet. So far, it is only set up to play one file")
#poggers
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if(message.author.bot):
        return
    if message.content == 'poggers' or message.content == "Poggers":
        response = 'lmao'
        await message.channel.send(response)
    await bot.process_commands(message)

#parrot       
@bot.command(help = "Repeats your message back to you")
async def parrot(ctx, *, chloroplast):
    await ctx.send(str(chloroplast))

#error handling

@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
            return
    ignored = (commands.CommandNotFound, )
    error = getattr(error, 'original', error)
    if isinstance(error, ignored):

        return
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Sorry, that is not a valid number of arguments for this command. If you need help understanding how this command works, please use the command %help (your command)')
    else:
        await ctx.send("error")

@bot.event
async def on_command(ctx):
    usertext = str(ctx.author)
    user = str(ctx.author.id)
    place = str(ctx.guild)
    existing = cursor.execute("SELECT number FROM bot_uses WHERE name = ?", (user,)).fetchone()
    try:
        existing = int(existing[0])
    except TypeError:
        existing = 0
    existing = int(existing) +1
    cursor.execute("INSERT INTO bot_uses(name,number) VALUES(?, ?) ON CONFLICT(name) DO UPDATE SET number=excluded.number", (user, existing))
    connection.commit()
    if existing == 1:
        await ctx.send("Thank you for using Sushibot for the first time! If you are confused in any way about what I can do, feel free to type %help or contact SushiInYourFace")
    if existing == 100:
        await ctx.send("This was your 100th Sushibot command! Congratulations!")
    print("New command from " + usertext + " in " + place)
    if existing == 250:
        await ctx.send("Congrats on your 250th Command to SushiBot")

@bot.command(help="RATS RATS RATS RATS RATS RATS RATS RATS RATS RATS RATS RATS", aliases=["rat", "RATS", "RAT"])
async def rats(ctx):
    rat = random.choice(open("RATSRATSRATS.txt").readlines())
    await ctx.send(rat)

bot.run(TOKEN)