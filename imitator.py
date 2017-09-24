#! python3

import discord
from discord.ext import commands
import asyncio

import time
import random
from urllib import request

prefix = 'test!'

bot = commands.Bot(command_prefix=prefix, description='Test Bot, Please Ignore')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    

@bot.command()
async def hello():
    """Bot says hello!"""
    await bot.say("Hello!")


@bot.command()
async def count(count : int):
    """Tries to count to whatever number you write."""
    if count < 21:    
        for x in range(1,count+1):
            await bot.say(x)
            asyncio.sleep(0.5)
    else:
        await bot.say("I can't count to " + str(count) + ".")


@bot.command()
async def roll(dice : str):
    """Rolls dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return
    
    if rolls > 100 or limit > 100000:
        await bot.say("Ehh, no. I am not going to roll " + str(rolls) + " d" + str(limit) +"!")
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command()
async def bank(operation : str, amount : int, recipient : str):
    """Ravenbank"""
    if operation == "transfer":
        await bot.say(str(amount) + " EUR transfered to " + recipient + ".")


@bot.command()
async def request(*, req : str):
    """Make a (feature) request."""
    with open("request.txt", "a") as requestFile:
        requestFile.write(req + "\n")
        await bot.say("Request received.")


@bot.command()
# Request (List)
async def requestList():
    """List all current requests."""
    with open("request.txt", "r") as requestFile:
        info = "Listing all requests.\n"
        content = requestFile.read()
        await bot.say(info + content)


@bot.command()
async def play(*, playing : str):
    """What should the bot be playing?"""
    await bot.change_presence(game=discord.Game(name=playing))
    await bot.say("I am now playing " + playing + ".")


@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool."""
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='@Imitator#2588')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, I am cool.')
    

@bot.command()
async def bash():
    """Quote from Bash.org."""
    quote = random.randint(0,8000)
    x = 0
    abort = 40000
    msg = 'Quote from Bash.org.\n'
    with open("bashorg", "r") as bashorg:
        while x <= quote:
            line = bashorg.readline()
            if line == '%\n':
                x += 1
                # print (x) # Debug
            elif x == quote:
                msg = msg + line
            abort -= 1
            # print (abort) # Debug
            if abort < 0:
                await bot.say("Fuck this! I'm out!")
                return
        await bot.say(msg)        


bot.run('MzYwNzY0NjUyMDEyOTYxODAz.DKgGog.vR_eLKlHw_wRsuU2ECM7fozK2CA')
