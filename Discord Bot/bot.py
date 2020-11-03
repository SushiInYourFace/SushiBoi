# bot.py
import os
import random
import datetime
from datetime import timedelta
import discord
from discord.ext import commands
import wolframalpha
import sqlite3

TOKEN = open("Discord_Token.txt").read()
WOLFRAM_KEY = open('Wolfram_Key.txt').read()
intents = discord.Intents.default()
intents.members = True
client = wolframalpha.Client(WOLFRAM_KEY)
bot = commands.Bot(command_prefix="%", intents=intents)

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_number (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_message (name TEXT PRIMARY KEY, message TEXT)")
connection.commit()

#on ready
@bot.event
async def on_ready():
    for guild in bot.guilds: 
        print("Connected to " + guild.name)
    await bot.change_presence(status = "Doin your mom")

    
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
#help 
@bot.command(help = "Displays some helpful advice")
async def helpme(ctx):
    await ctx.send("fuck you")
#horse    
@bot.command(help = "horse")
async def thehorse(ctx):
    await ctx.send(":horse:")
#fingering
@bot.command(help = "Displays helpful fingering charts", aliases = ["fingerchart", "fingeringchart"])
async def clarinetfingerings(ctx):
    response = discord.Embed(title = "Clarinet Fingerings")
    response.add_field(name="Standard Fingering Chart", value="https://bit.ly/fingermeuwu")
    response.add_field(name="Quarter Tone Chart", value="https://bit.ly/fingermedaddy")
    await ctx.send(embed = response)

#integer   
@bot.command(help = "Is it an integer? Let's find out!")
async def isinteger(ctx, arg):
    try:
        int(arg)
        await ctx.send("What do you think?")
    except ValueError:
        await ctx.send("Not an integer, dipshit")
#parrot       
@bot.command(help = "Repeats your message back to you")
async def parrot(ctx, *, chloroplast):
    await ctx.send(str(chloroplast))
#ping   
@bot.command(help = "displays current pingtime")
async def ping(ctx):
    pingtime= bot.latency * 1000
    pingtime= round(pingtime, 3)
    await ctx.send(content = "Current ping is " + str(pingtime) + " ms")
#roles baby
@bot.command(help = "displays a user's roles")
async def roles(ctx, member : discord.Member):
        member = [rolo.name for rolo in member.roles]
        member.remove("@everyone")
        await ctx.send("This user has the following roles: " + str(member))
#joindate    
@bot.command(help = "join date")
async def joined(ctx, *, member : discord.Member):
    embed1 = discord.Embed(title = str(member))
    embed1.add_field(name = "Joined server on", value = str(member.joined_at)[:-7] + " UTC")
    embed1.add_field(name = "Account created on", value = str(member.created_at)[:-7] + " UTC", inline = False)
    await ctx.send(embed = embed1)
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

#Wolfram
@bot.command(help = "Queries WolframAlpha")
async def wolfram(ctx, *, arg):
    async with ctx.channel.typing():
        try:
            res = client.query(arg)
            messagecontent = next(res.results).text
            validrep = True
        except:
            messagecontent = "Wolfram didn't like that input"
            validrep = False 
    if validrep == True:
        await ctx.send(("Input: {} \n{}".format(arg, messagecontent)))
    else:
        await ctx.send("Wolfram didn't like the input \"" + arg + "\"")
#user avatar    
@bot.command(help = "Displays a user avatar")
async def avatar(ctx, member : discord.Member):
    await ctx.send(str(member.avatar_url))

#SQL TEST
@bot.command(help = "Tests my implementation of SQL, currently no practical use.  \n To request current number associated with your account, add the argument \"query\"")
async def usernum(ctx, stringnum):
    sender = str(ctx.author)
    try:
        if stringnum == "query":
            output = cursor.execute("SELECT number FROM user_number WHERE name = ?", (sender,)).fetchone()
            await ctx.send(str(output[0]))
        else:
            int(stringnum)
            sender = str(ctx.author)
            arg = int(stringnum)
            cursor.execute("INSERT INTO user_number(name,number) VALUES(?, ?) ON CONFLICT(name) DO UPDATE SET number=excluded.number", (sender, arg))
            connection.commit()
            output = cursor.execute("SELECT number FROM user_number WHERE name = ?", (sender,)).fetchone()
            await ctx.send("Your new stored number is " + str(output[0]))
    except:
            await ctx.send("Sorry, this command requires an integer argument")

#user message store
@bot.command(help= 'Stores a personal message for each user. You can check a user\'s message with the querymessage command')
async def storemessage(ctx, *, arg):
    sender = str(ctx.author)
    cursor.execute("INSERT INTO user_message(name,message) VALUES(?, ?) ON CONFLICT(name) DO UPDATE SET message=excluded.message", (sender, arg))
    connection.commit()
    await ctx.send("Your new stored message is \"" + arg + "\"")
#user message query
@bot.command(help = "Shows the message a user has saved")
async def querymessage(ctx, *, member : discord.Member):
    try:
        targetuser = str(member)
        output = cursor.execute("SELECT message FROM user_message WHERE name = ?", (targetuser,)).fetchone()
        await ctx.send(str(output[0]))
    except:
        await ctx.send("This user has not created a message yet")

#test embed
@bot.command(help = "testing embeds")
async def embed(ctx):
    var23 = discord.Embed(title="Test Embed", color = 0x32a842)
    var23.add_field(name="Does this break anything?", value="Hopefully not!")
    await ctx.send(embed = var23)

#user info
@bot.command(help = "Lists information on a certain user")
async def userinfo(ctx, *, user : discord.Member):
    userembed = discord.Embed(title = str(user))
    userpic = str(user.avatar_url)
    userembed.set_thumbnail(url = userpic)
    nickname = user.nick
    userembed.add_field(name ="Nickname", value=nickname)
    userembed.add_field(name = "Joined Discord", value= str(user.created_at)[:-7] + " UTC", inline = False)
    userembed.add_field(name= "Joined server", value= str(user.joined_at)[:-7] + " UTC", inline = False)
    targetuser = str(user)
    storedmessage = cursor.execute("SELECT message FROM user_message WHERE name = ?", (targetuser,)).fetchone()
    userembed.add_field(name= "Stored message", value = storedmessage[0])
    userembed.add_field(name= "User ID", value= user.id)
    await ctx.send(embed = userembed)
bot.run(TOKEN)