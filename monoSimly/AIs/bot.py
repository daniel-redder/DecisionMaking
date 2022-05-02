import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from monoSimly.monopyly import *


import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def sendDM(target:discord.Member,message=""):
    embed = discord.Embed(title=message)
    await target.send(embed=embed)


#need to be after sendDM for runtime
from monoSimly.AIs.playerOne import playerOne as playerOneAI
from monoSimly.AIs.playerTwo import playerTwo as playerTwoAI


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} has connected to Discord!')
        print(f"{guild.name}")



@bot.command(context=True)
async def game(ctx,playerOne:discord.Member,playerTwo:discord.Member):
    print(ctx.message.author.name,playerOne,playerTwo)

    try:
        assert playerOne is not None and playerTwo is not None, "Please pass two arguments here"
    except:
        return


    await sendDM(playerOne,f"You have been invited to play a game against, {playerTwo.display_name}")
    await sendDM(playerTwo,f"You have been invited to play a game against, {playerOne.display_name}")

    await Logger.add_handler(FileLogHandler(f"data/{playerOne.display_name}_{playerTwo.display_name}_{random.randint(1,300)}.log", Logger.INFO))
    game = Game()
    playerOne_ai = playerOneAI(client,playerOne,bot)
    playerTwo_ai = playerTwoAI(client,playerTwo,bot)
    await game.add_player(playerOne_ai)
    await game.add_player(playerTwo_ai)
    await game.play_game()


bot.run(TOKEN)