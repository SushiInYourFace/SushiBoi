import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_number (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS bot_uses (name TEXT PRIMARY KEY, number INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_message (name TEXT PRIMARY KEY, message TEXT)")
connection.commit()

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
        #roles baby
    @commands.command(help = "displays a user's roles")
    async def roles(self, ctx, member : discord.Member):
            member = [rolo.name for rolo in member.roles]
            member.remove("@everyone")
            await ctx.send("This user has the following roles: " + str(member))

            #joindate    
    @commands.command(help = "join date")
    async def joined(self, ctx, *, member : discord.Member):
        embed1 = discord.Embed(title = str(member))
        embed1.add_field(name = "Joined server on", value = str(member.joined_at)[:-7] + " UTC")
        embed1.add_field(name = "Account created on", value = str(member.created_at)[:-7] + " UTC", inline = False)
        await ctx.send(embed = embed1)

    #user info
    @commands.command(help = "Lists information on a certain user")
    async def userinfo(self, ctx, *, user : discord.Member):
        userembed = discord.Embed(title = str(user))
        userpic = str(user.avatar_url)
        userembed.set_thumbnail(url = userpic)
        nickname = user.display_name
        userembed.add_field(name ="Nickname", value=nickname)
        userembed.add_field(name = "Joined Discord", value= str(user.created_at)[:-7] + " UTC", inline = False)
        userembed.add_field(name= "Joined server", value= str(user.joined_at)[:-7] + " UTC", inline = False)
        targetuser = str(user.id)
        userembed.add_field(name= "User ID", value= user.id)
        try:
            storedmessage = cursor.execute("SELECT message FROM user_message WHERE name = ?", (targetuser,)).fetchone()
            userembed.add_field(name= "Stored message", value = storedmessage[0])
        except TypeError:
            storedmessage = "This user has not stored a message yet"
            userembed.add_field(name= "Stored message", value = storedmessage)
        await ctx.send(embed = userembed)

    #user avatar    
    @commands.command(help = "Displays a user avatar")
    async def avatar(self, ctx, member : discord.Member):
        await ctx.send(str(member.avatar_url))

    @commands.command(help= "Displays how many times a user has used SushiBot", aliases = ["bot_uses", "uses"])
    async def botuses(self, ctx, *, member : discord.Member):
        plural = "s"
        try:
            targetuser = str(member.id)
            output = cursor.execute("SELECT number FROM bot_uses WHERE name = ?", (targetuser,)).fetchone()
            if int(output[0]) == 1:
                plural = ""
            await ctx.send("This user has used Sushibot " + str(output[0]) + " time" + plural)
        except TypeError:
            await ctx.send("This user has not used SushiBoi yet. Sad")

