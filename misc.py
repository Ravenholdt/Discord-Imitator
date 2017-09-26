import discord
from discord.ext import commands
import asyncio

import random


class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def hello(self, ctx):
        """Bot says hello!"""
        author = ctx.message.author.id
        await self.bot.say("Hello <@!{0}>!".format(author))


    @commands.command()
    async def roll(self, dice : str):
        """Rolls dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return
        
        if rolls > 100 or limit > 100000:
            await self.bot.say("Ehh, no. I am not going to roll " + str(rolls) + " d" + str(limit) +"!")
            return
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)


    @commands.command()
    async def request(self, *, req : str):
        """Make a (feature) request."""
        with open("data/request.txt", "a") as requestFile:
            requestFile.write(req + "\n")
            await self.bot.say("Request received.")


    @commands.command()
    # Request (List)
    async def requestList(self):
        """List all current requests."""
        with open("data/request.txt", "r") as requestFile:
            info = "Listing all requests.\n"
            content = requestFile.read()
            await self.bot.say(info + content)

def setup(bot):
    bot.add_cog(Misc(bot))