#pkmn_record_bot.py
#tl;dr – a bot that can create records in a DB and check stuff in the DB



##   GENERAL SETUP   ##
#import libraries that we will need access to
import discord
from discord.ext import commands
import json
import sqlite3

#connect to a (local) db via sqlite3
sql_conn = sqlite3.connect("pkmn_db.db")

#use a separate file to store the token
with open ("bot_token.json", "r") as read_file:
    bot_token = json.load(read_file)["test_bot"] #the specific bot



##  DISCORD SETUP ZONE  ##
#connect to discord via commnands.Bot(), the prefix is what the bot looks for (e.g. !hello, !check)
bot = commands.Bot(command_prefix = "!")

#called when the bot is connected to discord, show a message when successful
@bot.event
async def on_ready(): #this is a predefined function name!
    print ("\n{0.user} has been connected :D".format(bot))

#create a method for asking questions to reduce duplicate code
async def ask_question(ctx, question):
    #create a lambda to check that the reply was from op and is in the same channel so that the parameters passed are correct (cos the bot can answer itself LOL)
    check_msg = (lambda msg: msg.author == ctx.message.author and msg.channel == ctx.message.channel)

    await ctx.send(question)
    answer = await bot.wait_for('message', check=check_msg, timeout=60) #set the var to whatever the user replies
    return answer.content #get the message's content or it raises an error!



##  BOT COMMAND ZONE ##
#add a new record to the db
@bot.command()
async def create(ctx):
    user_id = ctx.message.author.id #get the user's id via ctx
    game_title = await ask_question(ctx, "What game is the pokemon team from?")

    pkmn_team = []
    for i in range(6):
        answer = await ask_question(ctx, f"Please add pokemon {str(i + 1)} on your team: ")
        pkmn_team.append(answer)

    await ctx.send(f"You have added {game_title} with: {', '.join(pkmn_team)}, for user {ctx.message.author}! :D") #for testing


    # #after getting the vars, put them into an SQL statement
    sql_create = f""" INSERT INTO user
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

    #cur is a SQL word, so u cant change the name
    cur = sql_conn.cursor()
    cur.execute(sql_create)
    sql_conn.commit()


#check what games a user has
@bot.command()
async def check(ctx):
    user_id = ctx.message.author.id
    sql_check = f"SELECT game_title from user WHERE user_id = '{str(user_id)}';"

    #connect to the db and retrieve the values based on the SELECT statement ^
    cur = sql_conn.cursor()
    cur.execute(sql_check)
    titles_list = cur.fetchall()

    print (user_id, titles_list)
    if titles_list == []:
        await ctx.send(f"The user {ctx.message.author} does not have any games registered :V")
    else:
        await ctx.send(f"The user {ctx.message.author} has these games registered: {', '.join(titles_list)}")


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


# def check(msg):
#     print (msg.author == ctx.message.author and msg.channel == ctx.message.channel)
#     return msg.author == ctx.message.author and msg.channel == ctx.message.channel
