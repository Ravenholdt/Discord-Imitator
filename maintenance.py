import discord
from discord.ext import commands
import asyncio

import os

import config


class Maintenance:
    def __init__(self, bot):
        self.bot = bot

    maint_loaded = True

    # this specifies what extensions to load when the bot starts up
    startup_extensions = ["silly","maths","info","misc","democracy"]
    extension_path = ""#"functions/"

    @commands.command()
    async def patch(self, devBranch = "development"):

        branch = ""
        if config.gitDev:
            branch = devBranch

        os.system("git pull origin " + branch)

        await self.loadAll()
        self.bot.say("System updated.")


    async def loadAll(self):
        for extension in self.startup_extensions:
            self.bot.unload_extensionU(self.extension_path + extension)
            try:
                self.bot.load_extension(self.extension_path + extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))


    @commands.command()
    async def load(self, extension_name : str):
        """Loads an extension."""
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.say("{} loaded.".format(extension_name))


    @commands.command()
    async def unload(self, extension_name : str):
        """Unloads an extension."""
        self.bot.unload_extension(extension_name)
        await self.bot.say("{} unloaded.".format(extension_name))


    @commands.command()
    async def reload(self, extension_name : str):
        """Reloads an extension."""
        self.bot.unload_extension(extension_name)
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.say("{} reloaded.".format(extension_name))

def setup(bot):
    bot.add_cog(Maintenance(bot))