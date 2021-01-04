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
import numpy as np



TOKEN = open("Discord_Token.txt").read()
WOLFRAM_KEY = open('Wolfram_Key.txt').read()
intents = discord.Intents.default()
intents.members = True
client = wolframalpha.Client(WOLFRAM_KEY)
bot = commands.Bot(command_prefix="%", intents=intents)


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

@bot.command(help = "disconnects the bot from whatever channel it is in")
async def leave(ctx):
    for client in bot.voice_clients:
        if client.guild == ctx.guild:
            await client.disconnect()

@bot.command(help = "Joins the voice channel you are currently in. Does not play anything", aliases = ["join"])
async def connect(ctx):
    channelname = ctx.author.voice.channel
    try: 
        vclient = await channelname.connect()
    except:
        pass

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
        vclient = await channelname.connect()
    except:
        pass
    resultant = discord.FFmpegPCMAudio(source="audiofilev2.wav", executable="C:\\Users\\Joel\\ffmpeg\\bin\\ffmpeg.exe")
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
        await ctx.send("Yes, that's an integer")
    except ValueError:
        await ctx.send("That's not an integer, dipshit")
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
@bot.command(help = "Not really anything useful, stores a number for each user.  \n To request current number associated with your account, add the argument \"query\". If you really want to store a number, you can do the same thing with the storemessage command.")
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
    except ValueError:
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

#user info
@bot.command(help = "Lists information on a certain user")
async def userinfo(ctx, *, user : discord.Member):
    userembed = discord.Embed(title = str(user))
    userpic = str(user.avatar_url)
    userembed.set_thumbnail(url = userpic)
    nickname = user.display_name
    userembed.add_field(name ="Nickname", value=nickname)
    userembed.add_field(name = "Joined Discord", value= str(user.created_at)[:-7] + " UTC", inline = False)
    userembed.add_field(name= "Joined server", value= str(user.joined_at)[:-7] + " UTC", inline = False)
    targetuser = str(user)
    userembed.add_field(name= "User ID", value= user.id)
    try:
        storedmessage = cursor.execute("SELECT message FROM user_message WHERE name = ?", (targetuser,)).fetchone()
        userembed.add_field(name= "Stored message", value = storedmessage[0])
    except:
        storedmessage = "This user has not stored a message yet"
        userembed.add_field(name= "Stored message", value = storedmessage)
    await ctx.send(embed = userembed)


@bot.command(help= "Displays how many times a user has used SushiBot", aliases = ["bot_uses", "uses"])
async def botuses(ctx, *, member : discord.Member):
    plural = "s"
    try:
        targetuser = str(member)
        output = cursor.execute("SELECT number FROM bot_uses WHERE name = ?", (targetuser,)).fetchone()
        if int(output[0]) == 1:
            plural = ""
        await ctx.send("This user has used Sushibot " + str(output[0]) + " time" + plural)
    except:
        await ctx.send("This user has not used SushiBoi yet. Sad")

@bot.event
async def on_command(ctx):
    user = str(ctx.author)
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
    print("New command from " + user + " in " + place)
    if existing == 250:
        await ctx.send("Congrats on your 250th Command to SushiBot")
"""
@bot.command(help = "Start a two player Connect-four game")
async def connect_four(ctx):
    output = discord.Embed(title = "Player 2, please react to this message to get started!")
    sent = await ctx.send(embed=output)
    started = discord.Embed(title = "This is where the game will be")
    await sent.add_reaction("✅")
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user != ctx.author and user != bot.user
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Game cancelled, No P2 reacted to the message")
    else:
        await ctx.send("Game started! (coming soon)")
        await sent.delete()
        truth = 1
    board = np.empty((6, 7), dtype=object)
    board.fill("-")
    turn = 2
    rows = [5, 4, 3, 2, 1, 0]
    cols = [6, 5, 4, 3, 2, 1, 0]
    def horizontal(game, column, rows):
        for y in column:
            for z in rows:
                    try:
                        if game[z, y] == game[z, y-1] == game[z, y-2] == game[z, y-3] != "-":
                            truth = 2
                            break
                    except IndexError:
                        pass

    def vertical(game, column, rows):
        for z in rows:
            for y in column:
                try:
                    if game[z, y] == game[z-1, y] == game[z-2, y] == game[z-3, y] != "-":
                        truth = 2
                        break
                except IndexError:
                    pass

    def diag1(game, column, rows):
        for y in column:
            for z in rows:
                try:
                    if game[z, y] == game[z-1, y-1] == game[z-2, y-2] == game[z-3, y-3] != "-":
                        truth = 2
                        break
                except IndexError:
                    pass

    def diag2(game, column, rows):
        for y in column:
            for z in rows:
                try:
                    if game[z, y] == game[z-1, y+1] == game[z-2, y+2] == game[z-3, y+3] != "-":

                        truth = 2
                        break
                except IndexError:
                    pass
    def play(col):
        for row in rows:
            if board[row, col-1] == "-":
                if turn % 2 == 0:
                    board[row, col-1] = "X"
                    break
                else:
                    board[row, col-1] = "O"
                    break
        print(str(board))
    while truth == 1:
        x = input()
        play(int(x))
        horizontal(board, cols, rows)
        vertical(board, cols, rows)
        diag1(board, cols, rows)
        diag2(board, cols, rows)
        if turn == 2:
            gameboard = discord.Embed(title = "Connect 4")
            gameboard.add_field(name = "Gameboard", value = str(board)[1:-1])
            current = await ctx.send(embed = gameboard)
        else:
            await current.delete()
            gameboard = discord.Embed(title = "Connect 4")
            gameboard.add_field(name = "Gameboard", value = "``` " + str(board)[1:-1] + "```")
            current = await ctx.send(embed = gameboard)
        turn += 1
    pass    
        """

    
bot.run(TOKEN)