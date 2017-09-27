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
        defs = ud.define(query)

        word = defs[0].word
        definition = defs[0].definition
        example = defs[0].example
        votes = str(defs[0].upvotes) + " | " + str(defs[0].downvotes)

        emb = discord.Embed(title=word)
        emb.add_field(name="Definition", value=definition, inline=False)
        emb.add_field(name="Example", value=str(example + "\n\n" + votes), inline=False)

        await self.bot.say(embed = emb)


def setup(bot):
    bot.add_cog(Info(bot))