import discord
from discord.ext import commands
import asyncio

import datetime

class Democracy:
    
    mot = "None."
    date = 0

    yes = []
    no = []
    abs = []

    lastMotionMsg = 0

    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True)
    async def motion(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.motionEmbed()
            

    @motion.command()
    async def new(self, *, motion : str):
        """Create a new motion."""
        if self.date == 0:
            self.mot = motion
            self.date = datetime.datetime.now()
            
        # Inform users that new motion started.
        await self.motionEmbed()
        


    async def motionEmbed(self, edit = False):
        if self.date == 0:
            await self.bot.say("No motion in progress.")
        else:
            embed=discord.Embed(title="Motion in progress")
            embed.add_field(name="------------------", value=self.mot, inline=False)
            value = "\U00002705 " + str(len(self.yes)) + "  |  \U0000274E " + str(len(self.no)) + "  |  \U00002611 " + str(len(self.abs))
            embed.add_field(name="Votes", value=value, inline=True)
            embed.set_footer(text=str(self.date))

            if edit:
                await self.bot.edit_message(self.lastMotionMsg, embed=embed)
            else:
                self.lastMotionMsg = await self.bot.say(embed=embed)




    @commands.group(pass_context=True)
    async def vote(self, ctx):
        """Vote!"""

    @vote.command(pass_context=True)
    async def yay(self, ctx):
        """Vote yes!"""
        if not self.date == 0:
            voter = ctx.message.author.id

            if voter in self.yes:
                return
            elif voter in self.no:
                self.no.remove(voter)
            elif voter in self.abs:
                self.abs.remove(voter)
            
            self.yes.append(voter)
            await self.bot.add_reaction(ctx.message, "\U00002705")

        await self.motionEmbed(True)

    @vote.command(pass_context=True)
    async def nay(self, ctx):
        """Vote no!"""
        if not self.date == 0:
            voter = ctx.message.author.id

            if voter in self.yes:
                self.yes.remove(voter)
            elif voter in self.no:
                return
            elif voter in self.abs:
                self.abs.remove(voter)
            
            self.no.append(voter)
            await self.bot.add_reaction(ctx.message, "\U0000274E")

        await self.motionEmbed(True)

    @vote.command(pass_context=True)
    async def abstain(self, ctx):
        """Beggars can't be choosers."""
        if not self.date == 0:
            voter = ctx.message.author.id

            if voter in self.yes:
                self.yes.remove(voter)
            elif voter in self.no:
                self.no.remove(voter)
            elif voter in self.abs:
                return

            self.abs.append(voter)
            await self.bot.add_reaction(ctx.message, "\U00002611")

        await self.motionEmbed(True)
        


def setup(bot):
    bot.add_cog(Democracy(bot))