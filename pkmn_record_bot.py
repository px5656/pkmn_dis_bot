#pkmn_record_bot.py
#tl;dr doesn'y do anything yet!

#import the library
import discord
from discord.ext import commands #access a more specific discord library that allows u to

#connect to discord via commnands.Bot (which works like client = discord.Client())
#the prefix lets the bot know what to look for
#and we also create a var for the SECRET token to connect to and run the bot itself
bot = commands.Bot(command_prefix = "!")
token = "" #blank for now


#called when the bot is connected to discord, show a message when successful
@bot.event
async def on_ready() #this is a prefefined function name, can't change this!!
    print ("{0.user} has been connected :D".format(bot))


client.run(token)
