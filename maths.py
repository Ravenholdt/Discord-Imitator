import discord
from discord.ext import commands
import asyncio

class Maths:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def math(self, ctx):
        """Does math."""

    @math.command()
    async def add(self, first : int, second : int):
        """Add Two numbers together"""
        await self.bot.say(first + second)

    @math.command()
    async def sub(self, first : int, second : int):
        """Subtract the second number from the first"""
        await self.bot.say(first - second)

    @math.command()
    async def multiply(self, first : int, second : int):
        """Multiply two numbers together"""
        await self.bot.say(first * second)

    @math.command()
    async def divide(self, first : float, second : float):
        """Divide the first number with the second"""
        await self.bot.say(first / second)

def setup(bot):
    bot.add_cog(Maths(bot))