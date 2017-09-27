import discord
from discord.ext import commands
import asyncio

import random


class Silly:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def count(self, count : int):
        """Tries to count to whatever number you write."""
        maxcount = 21
        if count < maxcount:    
            for x in range(1,count+1):
                await self.bot.say(x)
                asyncio.sleep(0.5)
        else:
            await self.bot.say("Yeah? Well, YOU count to " + str(count) + "!")


    @commands.command()
    async def play(self, *, playing : str):
        """What should the bot be playing?"""
        await self.bot.change_presence(game=discord.Game(name=playing))
        await self.bot.say("I am now playing " + playing + ".")

    
    @commands.group(pass_context=True)
    async def cool(self, ctx):
        """Says if a user is cool."""
        if ctx.invoked_subcommand is None:
            msg = 'No, {0.subcommand_passed} is not cool'.format(ctx)
            await self.bot.say(msg)

    @cool.command(name='bot')
    async def _bot(self):
        """Is the bot cool?"""
        await self.bot.say('Yes, I am cool.')


    @commands.command()
    async def bash(self):
        """Quote from Bash.org."""
        quote = random.randint(0,8000)
        x = 0
        abort = 40000
        msg = '**Quote from Bash.org.**\n'
        with open("data/bashorg", "r") as bashorg:
            while x <= quote:
                line = bashorg.readline()
                if line == '%\n':
                    x += 1
                elif x == quote:
                    msg = msg + line
                abort -= 1
                if abort < 0:
                    await self.bot.say("Fuck this! I'm out!")
                    return
            await self.bot.say(msg)


    @commands.command()
    async def internationale(self):
        with open("data/internationale.txt", "r") as lyrics:
            for line in lyrics:
                try:
                    await self.bot.say(line)
                except:
                    pass
                await asyncio.sleep(4)

    

def setup(bot):
    bot.add_cog(Silly(bot))