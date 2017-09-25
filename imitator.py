#! python3

import discord
from discord.ext import commands
import asyncio

import time
import random
from urllib import request

import config
prefix = '!'

# this specifies what extensions to load when the bot starts up
startup_extensions = ["silly","maths","wolfram","misc"]

bot = commands.Bot(command_prefix=prefix, description='Test Bot, Please Ignore')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')


@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))


@bot.command()
async def reload(extension_name : str):
    """Reloads an extension."""
    bot.unload_extension(extension_name)
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} reloaded.".format(extension_name))


#@bot.command(pass_context=True)
#async def hello(ctx):
#    """Bot says hello!"""
#    author = ctx.message.author.id
#    await bot.say("Hello <@!{0}>!".format(author))


#@bot.command()
#async def roll(dice : str):
#    """Rolls dice in NdN format."""
#    try:
#        rolls, limit = map(int, dice.split('d'))
#    except Exception:
#        await bot.say('Format has to be in NdN!')
#        return
#    
#    if rolls > 100 or limit > 100000:
#        await bot.say("Ehh, no. I am not going to roll " + str(rolls) + " d" + str(limit) +"!")
#        return
#    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
#    await bot.say(result)


@bot.command()
async def bank(operation : str, amount : int, recipient : str):
    """Ravenbank"""
    if operation == "transfer":
        await bot.say(str(amount) + " EUR transfered to " + recipient + ".")


#@bot.command()
#async def request(*, req : str):
#    """Make a (feature) request."""
#    with open("request.txt", "a") as requestFile:
#        requestFile.write(req + "\n")
#        await bot.say("Request received.")


#@bot.command()
#async def requestList():
#    """List all current requests."""
#    with open("request.txt", "r") as requestFile:
#        info = "Listing all requests.\n"
#        content = requestFile.read()
#        await bot.say(info + content)


#@bot.group(pass_context=True)
#async def cool(ctx):
#    """Says if a user is cool."""
#    if ctx.invoked_subcommand is None:
#        msg = 'No, {0.subcommand_passed} is not cool'.format(ctx)
#        await bot.say(msg)

#@cool.command(name='bot')
#async def _bot():
#    """Is the bot cool?"""
#    await bot.say('Yes, I am cool.')
    

#@bot.command()
#async def bash():
#    """Quote from Bash.org."""
#    quote = random.randint(0,8000)
#    x = 0
#    abort = 40000
#    msg = 'Quote from Bash.org.\n'
#    with open("bashorg", "r") as bashorg:
#        while x <= quote:
#            line = bashorg.readline()
#            if line == '%\n':
#                x += 1
#            elif x == quote:
#                msg = msg + line
#            abort -= 1
#            if abort < 0:
#                await bot.say("Fuck this! I'm out!")
#                return
#        await bot.say(msg)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config.discordtoken)
