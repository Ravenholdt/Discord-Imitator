import discord
from discord.ext import commands
import asyncio

import os

import config


class Maintenance:
    def __init__(self, bot):
        self.bot = bot

    # this specifies what extensions to load when the bot starts up
    startup_extensions = ["silly","maths","info","misc","democracy"]
    extension_path = ""#"functions/"

    @commands.command()
    async def update(self):

        branch = ""
        if config.gitDev:
            branch = "development"

        os.system("git pull origin " + branch)

        await self.loadAll()
        self.bot.say("System updated.")


    async def loadAll(self):
        for extension in self.startup_extensions:
            try:
                self.bot.load_extension(self.extension_path + extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))


    @commands.command()
    async def load(extension_name : str):
        """Loads an extension."""
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await bot.say("{} loaded.".format(extension_name))


    @commands.command()
    async def unload(extension_name : str):
        """Unloads an extension."""
        bot.unload_extension(extension_name)
        await bot.say("{} unloaded.".format(extension_name))


    @commands.command()
    async def reload(extension_name : str):
        """Reloads an extension."""
        bot.unload_extension(extension_name)
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await bot.say("{} reloaded.".format(extension_name))

def setup(bot):
    bot.add_cog(Maintenance(bot))