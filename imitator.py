#! python3

import discord
from discord.ext import commands
import asyncio

import os.system

import config
prefix = '!'

bot = commands.Bot(command_prefix=prefix, description='Test Bot, Please Ignore')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')


if __name__ == "__main__":
    try:
        extension = "maintenance"
        bot.load_extension(extension)
        bot.get_cog(extension).loadAll()
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))


    bot.run(config.discordtoken)
