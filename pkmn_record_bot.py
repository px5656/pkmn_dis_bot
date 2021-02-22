#pkmn_record_bot.py
#tl;dr – bit messy but can connect to a db and write to a db with simple commands!



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

    #check that the reply was from op and is in the same channel so that the parameters passed are correct!
    def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel


    await ctx.send(question)
    answer = await bot.wait_for('message', check=check, timeout=60)
    return answer.content



#add a new record to the db
@bot.command()
async def create(ctx):
    user_id = ctx.message.author.id #get the user's id via ctx

    game_title = await ask_question(ctx, "What game is the pokemon team from?")

    pkmn_team = []
    for i in range(6):
        await ctx.send(f"Please add pokemon {str(i + 1)} on your team: ")
        pkmn = await bot.wait_for('message', timeout=60)
        pkmn_team.append(pkmn.content)

    await ctx.send(f"You have added {game_title} with {pkmn_team}.") #for testing


    # #after getting the vars, put them into an SQL statement
    sql_statement = f""" INSERT INTO user
                         ('user_id',
                          'game_title',
                          'pkmn_1',
                          'pkmn_2',
                          'pkmn_3',
                          'pkmn_4',
                          'pkmn_5',
                          'pkmn_6')
                         VALUES('{str(user_id)}',
                                '{game_title}',
                                '{pkmn_team[0]}',
                                '{pkmn_team[1]}',
                                '{pkmn_team[2]}',
                                '{pkmn_team[3]}',
                                '{pkmn_team[4]}',
                                '{pkmn_team[5]}');
                     """

    #cur is a SQL word, so u cant change the name :'v
    cur = sql_conn.cursor()
    cur.execute(sql_statement)
    sql_conn.commit()


#connect to the bot via the secret token and bot ahoy!
bot.run(bot_token)




## EXTRA STUFF ##

# @bot.command()
# async def add(ctx, game_title):
#     await ctx.send(f"The game title is {game_title}")

# @bot.command()
# async def add(ctx):
#     await ctx.send("Question here :3")
#     var = await bot.wait_for('message', timeout=time to wait)


###if statement
# if team_amount == 0:
#     await ctx.send("You need to have at least one pokemon! :O")
# elif team_amount > 6:
#     await ctx.send("That's too many pokemon! You can have between 1 and 6 pokemon on your team.")

#dynamic team amount
# pkmn_team = []
# for i in range(int(team_amount.content)):
#     await ctx.send(f"Please add pokemon {str(i + 1)} on your team: ")
#     pkmn = await bot.wait_for("message", timeout=60)
#     pkmn_team.append(pkmn.content)


#     await ctx.send("What game are you adding?")
#     game_title = await bot.wait_for('message', timeout=60)
