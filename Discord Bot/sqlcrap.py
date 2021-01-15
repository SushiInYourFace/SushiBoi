import discord
from discord.ext import commands
import sqlite3


connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_number (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS bot_uses (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_message (name TEXT PRIMARY KEY, message TEXT)")
connection.commit()

class SQLCrap(commands.Cog, name="SQL Crap"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        
    @commands.command(help = "Not really anything useful, stores a number for each user.  \n To request current number associated with your account, add the argument \"query\". If you really want to store a number, you can do the same thing with the storemessage command.")
    async def usernum(self, ctx, stringnum):
        sender = str(ctx.author.id)
        try:
            if stringnum == "query":
                output = cursor.execute("SELECT number FROM user_number WHERE name = ?", (sender,)).fetchone()
                await ctx.send(str(output[0]))
            else:
                int(stringnum)
                sender = str(ctx.author.id)
                arg = int(stringnum)
                cursor.execute("INSERT INTO user_number(name,number) VALUES(?, ?) ON CONFLICT(name) DO UPDATE SET number=excluded.number", (sender, arg))
                connection.commit()
                output = cursor.execute("SELECT number FROM user_number WHERE name = ?", (sender,)).fetchone()
                await ctx.send("Your new stored number is " + str(output[0]))
        except ValueError:
                await ctx.send("Sorry, this command requires an integer argument")

        
    #user message store
    @commands.command(help= 'Stores a personal message for each user. You can check a user\'s message with the querymessage command')
    async def storemessage(self, ctx, *, arg):
        sender = str(ctx.author.id)
        cursor.execute("INSERT INTO user_message(name,message) VALUES(?, ?) ON CONFLICT(name) DO UPDATE SET message=excluded.message", (sender, arg))
        connection.commit()
        await ctx.send("Your new stored message is \"" + arg + "\"")
    
    #user message query
    @commands.command(help = "Shows the message a user has saved")
    async def querymessage(self, ctx, *, member : discord.Member):
        try:
            targetuser = str(member.id)
            output = cursor.execute("SELECT message FROM user_message WHERE name = ?", (targetuser,)).fetchone()
            await ctx.send(str(output[0]))
        except TypeError:
            await ctx.send("This user has not created a message yet")