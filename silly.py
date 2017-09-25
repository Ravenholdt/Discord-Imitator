import discord
from discord.ext import commands
import asyncio

class Silly:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def count(self, count : int):
        """Tries to count to whatever number you write."""
        if count < 21:    
            for x in range(1,count+1):
                await self.bot.say(x)
                asyncio.sleep(0.5)
        else:
            await self.bot.say("I can't count to " + str(count) + ".")


def setup(bot):
    bot.add_cog(Silly(bot))