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
        #res = 'Please ignore this function.'
        answer = next(res.results).text
        await self.bot.say("From Wolfram Alpha:\n" + answer)


def setup(bot):
    bot.add_cog(Wolfram(bot))