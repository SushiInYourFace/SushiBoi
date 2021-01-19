import discord
from discord.ext import commands
from discord.errors import ClientException

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    #leave command
    @commands.command(help = "disconnects the bot from whatever channel it is in")
    async def leave(self, ctx):
        for client in self.bot.voice_clients:
            if client.guild == ctx.guild:
                await client.disconnect()
            
    #join command
    @commands.command(help = "Joins the voice channel you are currently in. Does not play anything", aliases = ["join"])
    async def connect(self, ctx):
        try: 
            channelname = ctx.author.voice.channel
            await channelname.connect()
        except AttributeError:
            await ctx.send("You don't appear to be in a voice channel!")
        except ClientException:
            await ctx.send("I'm already in a voice channel!")
            
    #TTS messages, have not completed
    @commands.command(help = "Reads your message in the voice channel you are currently in")
    async def read(self, ctx, *, arg):
        if (str(type(ctx.author.voice))) == "<class 'NoneType'>":
            await ctx.send("Not connected to a channel!")
        else:
            await ctx.send("Sorry, I haven't made this command yet")

    #may be safe to get rid of this at some point soon
    @commands.command (help="Testing a voice command")
    async def voicetest(self, ctx):
        try:
            channelname = ctx.author.voice.channel
            try:
                await channelname.connect()
            except(AttributeError, ClientException):
                pass
            resultant = discord.FFmpegPCMAudio(source="audiofilev2.wav", executable="/usr/bin/ffmpeg")
            ctx.voice_client.play(resultant)
            await ctx.send("This is not a finished command yet. So far, it is only set up to play one file")
        except AttributeError:
            await ctx.send("You don't seem to be in a voice channel!")


def setup(bot):
    bot.add_cog(Voice(bot))