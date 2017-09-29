import discord
from discord.ext import commands
import asyncio

import datetime

class Motion(object):
    
#    motion = "None." # Keeps track of the current Motion.
#    date = 0 # Keeps track of when the current motion started.
#    proposalBy = 0

    # Ballot
    yes = []
    no = []
    abs = []

    lastMsg = [] # List of all Motion embeds for editing.

    def __init__(motion, proposalBy):
        self.motion = motion
        self.proposalBy = proposalBy
        self.date = datetime.datetime.now()


class Democracy:
    
    mot = 0

    approvalNeeded = 2 # How many "yes" is needed to pass a vote.
    numberOfBots = 1 #2 # DEBUG

    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True)
    async def motion(self, ctx):
        """View current motion or create a new one."""
        if ctx.invoked_subcommand is None:
            await self.motionHandler()
            

    @motion.command(pass_context=True)
    async def new(self, ctx, *, motion : str):
        """Create a new motion."""
        if self.mot == 0:
            self.mot = Motion(motion = motion, proposalBy = ctx.message.author.id)
            
        # Inform users that new motion started.
        await self.motionHandler()
        

    async def motionHandler(self, edit = False):
        """Motion handler."""
        if self.mot == 0:
            await self.bot.say("No motion in progress.")
        else:
            await self.motionEmbed(edit = edit)

#            users = int(self.bot.servers[0].member_count) - self.numberOfBots
#            self.approvalNeeded = (users / 2) #+ 1 # DEBUG

            # Checks for approval.
            if len(self.yes) >= self.approvalNeeded:
                # Vote passes
                await self.motionEmbed(edit = True, status = "Passed.") # Edit all previous Embeds
                await self.motionEmbed(edit = False, status = "Passed.") # Create an ending embed.
                await self.resetMotion(passed = True) # Reset the voting.

            # Checks for disapproval.
            if len(self.no) >= self.approvalNeeded:
                # Vote failed
                await self.motionEmbed(edit = True, status = "Failed.") # Edit all previous Embeds
                await self.motionEmbed(edit = False, status = "Failed.") # Create an ending embed.
                await self.resetMotion(passed = False) # Reset the voting.


    async def motionEmbed(self, edit = False, status = "in progress."):
        """Motion display."""

        # Create the embed
        embTitle = "Motion " + status
        embed=discord.Embed(title=embTitle)
        embed.add_field(name="------------------", value=self.mot.motion, inline=False)
        value = "\U00002705 " + str(len(self.mot.yes)) + "  |  \U0000274E " + str(len(self.mot.no)) + "  |  \U00002611 " + str(len(self.mot.abs))
        embed.add_field(name="Votes", value=value, inline=True)
        embed.set_footer(text= "Proposal by: <@" + self.mot.proposalBy + ">  " + str(self.mot.date))

        if edit: # Update already existing embed
            for motionMsg in self.mot.lastMsg:
                    await self.bot.edit_message(motionMsg, embed=embed)
        else: # Create a new embed
            motMsg = await self.bot.say(embed=embed)
            self.mot.lastMsg.append(motMsg)
                

    async def resetMotion(self, passed = False):
        """Resets the voting."""

        # If the motion passed
        if passed == True:
            
            # Keep track of the number of laws.
            lawNR = 0
            with open("var/motionsNR.txt", "r") as file:
                lawNR = int(file.readline()) # Read current law number from file.
            lawNR += 1
            with open("var/motionsNR.txt", "w") as file:
                file.write(str(lawNR)) # Save passed law number to file

            # Save the new law.
            with open("var/motions.txt", "a") as file:
                msg = "**$" + str(lawNR) + ":** " + self.mot + "\n**Proposal by:** <@" + self.proposalBy + ">\n - Votes: "

                msg += "For: "
                for voter in self.mot.yes:
                    msg += "<@" + voter + ">, "

                msg += " Against: "
                for voter in self.mot.no:
                    msg += "<@" + voter + ">, "

                msg += " Abstain: "
                for voter in self.mot.abs:
                    msg += "<@" + voter + ">, "

                file.write(msg + "\n")


        # Clear the motion.
        self.mot = 0



    @commands.group(pass_context=True)
    async def vote(self, ctx):
        """Vote!"""

    @vote.command(pass_context=True)
    async def yay(self, ctx):
        """Vote yes!"""
        await self.votingHandler(ctx, "yay")

    @vote.command(pass_context=True)
    async def nay(self, ctx):
        """Vote no!"""
        await self.votingHandler(ctx, "nay")

    @vote.command(pass_context=True)
    async def abstain(self, ctx):
        """Beggars can't be choosers."""
        await self.votingHandler(ctx, "abstain")


    async def votingHandler(self, ctx, ballot : str):
        """Voting handler."""
        if not self.mot == 0:
            voter = ctx.message.author.id # Get id of the voter

            if voter in self.yes:
                self.yes.remove(voter)
            elif voter in self.no:
                self.no.remove(voter)
            elif voter in self.abs:
                self.abs.remove(voter)
            
            if ballot == "yay":
                self.yes.append(voter)
                await self.bot.add_reaction(ctx.message, "\U00002705") # Yes

            elif ballot == "nay":
                self.no.append(voter)
                await self.bot.add_reaction(ctx.message, "\U0000274E") # No

            elif ballot == "abstain":
                self.abs.append(voter)
                await self.bot.add_reaction(ctx.message, "\U00002611") # Abstain

        await self.motionHandler(edit = True)


    @commands.command()
    async def resolutions(self):
        """View the resolutions."""
        with open("var/motions.txt", "r") as file:
            data = file.read()
            if data == "":
                await self.bot.say("There are no resolutions yet.")
            else:
                await self.bot.say(data)
            

def setup(bot):
    bot.add_cog(Democracy(bot))