import discord
import globals
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    @commands.command(help="toggles debugmode")
    async def debug(self, ctx):
        globals.debugmode = not globals.debugmode
        state = "on" if globals.debugmode else "off"
        await ctx.send("Debug mode is now " + state)
    @commands.command(help="Checks to see if debug mode is on")
    async def debugcheck(self, ctx):
        await ctx.send(globals.debugmode)



        