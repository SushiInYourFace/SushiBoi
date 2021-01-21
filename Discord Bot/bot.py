# bot.py
import os
import sys
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
import globals
import json
import traceback
from discord.errors import ClientException

#initiating different clients and tokens
TOKEN = open("Discord_Token.txt").read()
WOLFRAM_KEY = open('Wolfram_Key.txt').read()
client = wolframalpha.Client(WOLFRAM_KEY)
pokeclient = pokepy.V2Client()

#intents, starting bot
async def get_pre(bot, message):
    prefixes = ["%"]
    try:
         guildcommand = cursor.execute("SELECT prefix FROM guild_prefixes WHERE guild = ?", (message.guild.name,)).fetchone()
         prefixes.append(str(guildcommand[0]))
    except TypeError:
        pass
    return prefixes

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_pre, intents=intents)

#SQLite
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_number (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS bot_uses (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_message (name TEXT PRIMARY KEY, message TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS command_uses (command TEXT PRIMARY KEY, uses INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS guild_prefixes (guild TEXT PRIMARY KEY, prefix TEXT)")
connection.commit()

#JSON writer, used for logging messages
def writer(data, filename='messages.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

#on ready
@bot.event
async def on_ready():
    globals.load()
    for guild in bot.guilds: 
        print("Connected to " + guild.name)

#cogs
initial_extensions = [
    'cogs.cmty',
    'cogs.info',
    'cogs.Responses',
    'cogs.sqlcrap',
    'cogs.userinfo',
    'cogs.util',
    'cogs.voice']

for extension in initial_extensions:
    bot.load_extension(extension)


#poggers
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if(message.author.bot):
        return
 #   if message.content == 'poggers' or message.content == "Poggers":
      #  response = 'lmao'
       # await message.channel.send(response)
    await bot.process_commands(message)

#error handling
@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
            return
    ignored = (commands.CommandNotFound, )
    error = getattr(error, 'original', error)
    #ignores ignored errors
    if isinstance(error, ignored):
        return
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Sorry, that is not a valid number of arguments for this command. If you need help understanding how this command works, please use the command %help (your command)')
    else:
        await ctx.send("error")
    #records tracebacks
    er = traceback.extract_stack()
    strerror = er.format()
    result = ""
    for item in strerror:
        result += item
    #checks if debug mode is on
    if globals.debugmode == True:
        #checks if I sent the message
        if ctx.author.id == 523655829279342593:
            await ctx.send("```" + str(error) + "\n" + result + "```")
        else:
            await ctx.send("Because debug mode is on, your traceback was saved")

@bot.event
async def on_command(ctx):
    usertext = str(ctx.author)
    intid = ctx.author.id
    user = str(ctx.author.id)
    place = str(ctx.guild)
    command = ctx.command.name
    existing = cursor.execute("SELECT number FROM bot_uses WHERE name = ?", (user,)).fetchone()
    #checks if the user is already in the database
    try:
        existing = int(existing[0])
    except TypeError:
        existing = 0
    existing = int(existing) +1
    #makes sure the command is in a cog, and sets the variable accordingly
    try:
        cog = ctx.cog.qualified_name,
    except AttributeError: 
        cog = "None"
    #checks if the command has been used
    prev_uses = cursor.execute("SELECT uses FROM command_uses WHERE command = ?", (command,)).fetchone()
    try:
        prev_uses = int(prev_uses[0])
    except TypeError:
        prev_uses = 0
    prev_uses = int(prev_uses)+1
    #adds new command uses
    cursor.execute("INSERT INTO command_uses(command,uses) VALUES(?, ?) ON CONFLICT(command) DO UPDATE SET uses=excluded.uses", (command, prev_uses))
    #adds user to database if needed
    cursor.execute("INSERT INTO users(id,name) VALUES(?, ?) ON CONFLICT(id) DO UPDATE SET name=excluded.name", (intid, usertext))
    #adds one to the user's count
    cursor.execute("INSERT INTO bot_uses(name,number) VALUES(?, ?) ON CONFLICT(name) DO UPDATE SET number=excluded.number", (user, existing))
    #milestone messages
    connection.commit()
    if existing == 1:
        await ctx.send("Thank you for using Sushibot for the first time! If you are confused in any way about what I can do, feel free to type %help or contact SushiInYourFace")
    if existing == 100:
        await ctx.send("This was your 100th Sushibot command! Congratulations!")
    if existing == 250:
        await ctx.send("Congrats on your 250th Command to SushiBot")
    #prints to console
    print("New command from " + usertext + " in " + place)
    #Adds message to JSON
    with open('messages.json') as jfile:
        data = json.load(jfile)
        coms = data['commands']
        ndata = {
             "User": usertext,
             "Guild": place,
             "Channel": str(ctx.channel),
             "Command": command,
             "Cog": cog,
             "Time": str(datetime.datetime.now())
        }
        coms.append(ndata)
    writer(data)


bot.run(TOKEN)