#pkmn_record_bot.py
#tl;dr – connects to db and can do a simple command



##   SETUP   ##
#import the discord library, access a specific part of the discord.ext library and json library
import discord
from discord.ext import commands
import json
import sqlite3

#connect to a (local) database via sqlite3
sql_conn = sqlite3.connect("pkmn_db.db")



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


#create a method to ask qursitons neater
async def ask_question(ctx, question):
    await ctx.send(question)
    answer = await bot.wait_for("message", timeout=60)
    return answer.content


#add a new record to the db
@bot.command()
async def create(ctx):
    user_id = ctx.message.author.id #get the user's id via ctx

    await ctx.send("What game are you adding?")
    game_title = await bot.wait_for("message", timeout=60)


    await ctx.send("How many pokemon are on your team?")
    team_amount = await bot.wait_for("message", timeout=60)


    pkmn_team = []
    for i in range(int(team_amount.content)):
        await ctx.send(f"Please add pokemon {str(i + 1)} on your team: ")
        pkmn = await bot.wait_for("message", timeout=60)
        pkmn_team.append(pkmn.content)

    # if team_amount == 0:
    #     await ctx.send("You need to have at least one pokemon! :O")
    # elif team_amount > 6:
    #     await ctx.send("That's too many pokemon! You can have between 1 and 6 pokemon on your team.")

    await ctx.send(f"You have added {game_title.content} with {pkmn_team}.") #for testing



# @bot.command()
# async def add(ctx, game_title):
#     await ctx.send(f"The game title is {game_title}")

# @bot.command()
# async def add(ctx):
#     await ctx.send("Question here :3")
#     var = await bot.wait_for('message', timeout=time to wait)



bot.run(bot_token)
