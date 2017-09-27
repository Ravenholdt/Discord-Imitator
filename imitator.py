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
startup_extensions = ["silly","maths","info","misc","democracy"]

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


@bot.command()
async def bank(operation : str, amount : int, recipient : str):
    """Ravenbank"""
    if operation == "transfer":
        await bot.say(str(amount) + " EUR transfered to " + recipient + ".")


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config.discordtoken)
