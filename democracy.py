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

    approvalNeeded = 3 # How many "yes" is needed to pass a vote.
    lastMotionMsg = []

    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True)
    async def motion(self, ctx):
        """View current motion or create a new one."""
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
        """Motion handler"""
        if self.date == 0:
            await self.bot.say("No motion in progress.")
        else:
            # Create the embed
            embed=discord.Embed(title="Motion in progress")
            embed.add_field(name="------------------", value=self.mot, inline=False)
            value = "\U00002705 " + str(len(self.yes)) + "  |  \U0000274E " + str(len(self.no)) + "  |  \U00002611 " + str(len(self.abs))
            embed.add_field(name="Votes", value=value, inline=True)
            embed.set_footer(text=str(self.date))

            if edit:
                await self.bot.edit_message(self.lastMotionMsg, embed=embed)
            else:
                self.lastMotionMsg = await self.bot.say(embed=embed)

            # Checks for approval.
            if len(self.yes) >= self.approvalNeeded:
                # Vote passes
                await self.bot.say("**Motion:**\n" + self.mot + "\n **Passed.**")
                await self.resetMotion(True)

            if len(self.no) >= self.approvalNeeded:
                # Vote failed
                await self.bot.say("**Motion:**\n" + self.mot + "\n **Failed.**")
                await self.resetMotion(False)
            if edit: # Update already existing embed
                for motionMsg in self.lastMotionMsg:
                        await self.bot.edit_message(self.lastMotionMsg, embed=embed)
            else: # Create a new embed
                self.lastMotionMsg.append = await self.bot.say(embed=embed)
                

    async def resetMotion(self, passed = False):

        lawNR = 0

        # If the motion passed
        if passed == True:
            with open("var/motionsNR.txt", "r+") as file:
                lawNR = int(file.readline())
                lawNR += 1
                file.write(lawNR)
            with open("var/motions.txt", "a") as file:
                msg = "$" + lawNR + ": " + self.mot + "\n - Votes: "
                msg += "For: "
                for voter in self.yes:
                    msg += "<@" + voter + ">, "
                    self.yes.remove(voter)

                msg += " Against: "
                for voter in self.no:
                    msg += "<@" + voter + ">, "
                    self.no.remove(voter)

                msg += " Abstain: "
                for voter in self.abs:
                    msg += "<@" + voter + ">, "
                    self.abs.remove(voter)
        
        # If the motion failed
        else:
            for voter in self.yes:
                self.yes.remove(voter)
            for voter in self.no:
                self.no.remove(voter)
            for voter in self.abs:
                self.abs.remove(voter)

        for motionMsg in self.lastMotionMsg:
            self.lastMotionMsg.remove(motionMsg)
        self.date = 0
        self.mot = "None."



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