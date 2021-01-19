import discord
from discord.ext import commands
import asyncio
from discord import abc
from discord.abc import Messageable
from discord.colour import Colour

class Community(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(help= "Creates a poll which lasts a minute", aliases=["voting", "poll"])
    async def vote(self, ctx, *, arg):
        vote = discord.Embed(title=arg)
        poll = await ctx.send(embed=vote)
        pollid = poll.id
        await poll.add_reaction("👍")
        await poll.add_reaction("👎")
        await asyncio.sleep(60)
        finalpoll = await ctx.fetch_message(id=pollid)
        reacts = finalpoll.reactions
        numyes = 0
        numno = 0
        nummisc = 0
        for react in reacts:
            if react.emoji == "👍":
                numyes = react.count - 1
            elif react.emoji == "👎":
                numno = react.count - 1
            else:
                nummisc += react.count

        await poll.delete()
        rex = "Results- "
        if numyes >> numno:
            results = discord.Embed(title=rex + arg, color=0x008000)
        elif numno >> numyes:
            results = discord.Embed(title=rex + arg, color=0xFF0000)
        else:
            results = discord.Embed(title=rex + arg, color=0x0000FF)
        results.add_field(name="Yes: ", value=numyes)
        results.add_field(name="No: ", value=numno)
        if nummisc != 0:
            results.add_field(name="Misc. Reactions", value=nummisc)
        await ctx.send(embed=results)
        
def setup(bot):
    bot.add_cog(Community(bot))