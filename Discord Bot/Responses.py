import discord
from discord.ext import commands

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command(help = "The Horse")
    async def thehorse(self, ctx):
        await ctx.send(":horse:")
    
    @commands.command(help = "Displays some helpful advice")
    async def helpme(self, ctx):
        await ctx.send("fuck you")

    @commands.command(help = "Displays helpful fingering charts", aliases = ["fingerchart", "fingeringchart"])
    async def clarinetfingerings(self, ctx):
        response = discord.Embed(title = "Clarinet Fingerings")
        response.add_field(name="Standard Fingering Chart", value="https://bit.ly/fingermeuwu")
        response.add_field(name="Quarter Tone Chart", value="https://bit.ly/fingermedaddy")
        await ctx.send(embed = response)

        #parrot       
    @commands.command(help = "Repeats your message back to you")
    async def parrot(self, ctx, *, arg):
        await ctx.send(str(arg))