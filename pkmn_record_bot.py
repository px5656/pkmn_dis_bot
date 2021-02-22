#pkmn_record_bot.py
#tl;dr doesn'y do anything yet!

##   SETUP   ##
#import the discord library, access a specific part of the discord.ext library and json library
import discord
from discord.ext import commands
import json


##   JSON ZONE  ##
#we create a var for the SECRET token to connect to and run the bot itself
#access via JSON file since it should be...SECRET!!! don't commit it LOL!!!
with open ("bot_token.json", "r") as read_file:
    bot_token = json.load(read_file)["test_bot"] #the specific bot



##  DISCORD ZONE  ##
#connect to discord via commnands.Bot (which works like client = discord.Client())
#prefix = what the bot looks for (e.g. !hello, !check)
bot = commands.Bot(command_prefix = "!")


#called when the bot is connected to discord, show a message when successful
@bot.event
async def on_ready(): #this is a predefined function name, can't change this!!
    print ("{0.user} has been connected :D".format(bot))


@bot.command()
async def add(ctx, game_title):
    await ctx.send(f"The game title is {game_title}")



bot.run(bot_token)
