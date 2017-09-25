import discord
from discord.ext import commands
import asyncio

import wolframalpha
import wikipedia
import urbandictionary as ud

import config

client = wolframalpha.Client(config.wolframappid)

class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wolfram(self, *, query : str):
        """Ask Wolfram Alpha."""
        res = client.query(query)
        #res = 'Please ignore this function.'
        answer = next(res.results).text
        await self.bot.say("**From Wolfram Alpha:**\n" + answer)


    @commands.command()
    async def wikipedia(self, *, query : str):
        """Search the Wikipedia."""
        page = wikipedia.page(query)
        summary = wikipedia.summary(query)
        msg = "**"+page.title+"**\n"+summary+"\n"+page.url
        await self.bot.say(msg)


    @commands.command()
    async def urban(self, *, query : str):
        """Search the Urban Dictionary."""
        msg = "**From Urban Dictionary:**\n"
        defs = ud.define(query)
        for d in defs:
            msg = msg + "**" + defs[0].word + ":** " + d.definition + "\n"
        await self.bot.say(msg)


def setup(bot):
    bot.add_cog(Info(bot))