import discord
from discord.ext import commands
import asyncio

import wolframalpha
import config

client = wolframalpha.Client(config.wolframappid)

class Wolfram:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wolfram(self, *, query : str):
        """Ask Wolfram Alpha."""
        res = client.query(query)
        self.bot.say(res)


def setup(bot):
    bot.add_cog(Wolfram(bot))