import discord
import globals
from discord.ext import commands
import Notifs
from tkinter import *

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
    @commands.command(help="Sends a message to Sushi's desktop", aliases=["notif", "sendnotif", "notifications"])
    async def notification(self, ctx, *, arg):
        Notifs.send(arg)
        await ctx.send("Your notification was sent!")
    
    #TKinter window letting me send a message as SushiBot
    @commands.command(help="Currently only useable by Sushi, allows the sending of a message as the bot")
    async def sendas(self, ctx):
        #makes sure it's me sending the message
        if ctx.author.id == 523655829279342593:
            #sets up window
            window = Tk()
            window.title("Sick-ass GUI")
            window.geometry('800x450')
            leftframe = Frame(window)
            #executes when guild is confirmed
            def onclick():
                pos = lst.curselection()
                selected = lst.get(pos)
                print(selected)
                for guild in self.bot.guilds:
                    if guild.name == selected:
                        selectedguild = guild
                        break
                if selectedguild:
                    for channel in selectedguild.text_channels:
                        chnls.insert(END, channel.name)

            #sets up items in window
            lst = Listbox(leftframe, height=7, width=25)
            guildsubmit = Button(leftframe, text="Submit Guild", command=onclick)
            chnls = Listbox(window)
            chnlsubmit = Button(window, text="Submit Channel")
            #adds items to guild listbox
            for guild in self.bot.guilds:
                lst.insert(END, guild.name)
            #draws the items to the window
            leftframe.pack(side=LEFT, fill=Y)
            lst.pack(side=TOP)
            guildsubmit.pack(side=TOP)
            chnls.pack(side=TOP)
            await ctx.send("GUI Opened!")
            window.mainloop()

                        
        else:
            await ctx.send("Sorry, Sushi is currently the only person able to use this command")

def setup(bot):
    bot.add_cog(Utility(bot))

        