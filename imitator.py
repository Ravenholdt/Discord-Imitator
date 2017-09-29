#! python3

import discord
from discord.ext import commands
import asyncio

import time

import config
prefix = '!'

bot = commands.Bot(command_prefix=prefix, description='Test Bot, Please Ignore')


@bot.event
async def on_ready():
    await bot.get_cog("Maintenance").loadAll()
    print('Logged in as')
    print(bot.user.name)
    print('------')

async def maintCheck():
    """Make sure Maintenance is always running."""
    await bot.wait_until_ready()
    while True:
        await asyncio.sleep(10)
        try:
            if bot.get_cog("Maintenance").maint_loaded:
                pass
        except:
            loadMaint()

def loadMaint():
    try:
        bot.load_extension("maintenance")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

if __name__ == "__main__":
    loadMaint()

    bot.loop.create_task(maintCheck())
    bot.run(config.discordtoken)
