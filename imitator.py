#! python3

import discord
from discord.ext import commands
import asyncio

import time

import config
prefix = '!'

bot = commands.Bot(command_prefix=prefix, description='Test Bot, Please Ignore')

extension = "maintenance"

@bot.event
async def on_ready():
    await bot.get_cog("Maintenance").loadAll()
    print('Logged in as')
    print(bot.user.name)
    print('------')


if __name__ == "__main__":
    try:
        bot.load_extension(extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config.discordtoken)
