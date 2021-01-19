import discord
from discord.ext import commands
import wolframalpha
import pokepy
from discord import client
from beckett.exceptions import InvalidStatusCodeError

pokeclient = pokepy.V2Client()
WOLFRAM_KEY = open('Wolfram_Key.txt').read()
client = wolframalpha.Client(WOLFRAM_KEY)


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    #integer   
    @commands.command(help = "Is it an integer? Let's find out!")
    async def isinteger(self, ctx, arg):
        try:
            int(arg)
            await ctx.send("Yes, that's an integer")
        except ValueError:
            await ctx.send("That's not an integer, dipshit")

    #wolfram
    @commands.command(help = "Queries WolframAlpha")
    async def wolfram(self, ctx, *, arg):
        async with ctx.channel.typing():
            try:
                res = client.query(arg)
                messagecontent = next(res.results).text
                validrep = True
            except AttributeError:
                messagecontent = "Wolfram didn't like that input"
                validrep = False 
        if validrep == True:
            await ctx.send(("Input: {} \n{}".format(arg, messagecontent)))
        else:
            await ctx.send("Wolfram didn't like the input \"" + arg + "\"")

    @commands.command(help="Pokemon. Info. Hopefully not broken.")
    async def pokemon(self, ctx, arg):
        try:
            pokemon = pokeclient.get_pokemon(arg)
            species = pokeclient.get_pokemon_species(arg)
            returnembed = discord.Embed(title=pokemon.name)
            returnembed.add_field(name="ID", value=pokemon.id)
            returnembed.add_field(name="species", value=(species.name))
            returnembed.add_field(name="Generation", value=species.generation.name)
            await ctx.send(embed=returnembed)
        except InvalidStatusCodeError:
            await ctx.send("Not a valid pokemon")
        

def setup(bot):
    bot.add_cog(Information(bot))