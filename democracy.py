import discord
from discord.ext import commands
import asyncio

import datetime
import os.path
import os
import pickle

import config


class Motion:
    
    def __init__(self, newMotion, newProp):
        self.motion = newMotion
        self.proposalBy = newProp
        self.date = datetime.datetime.now()

        # Ballot
        self.yes = []
        self.no = []
        self.abs = []

        # List of all Motion embeds for editing.
        self.lastMsg = []


class Democracy:
    
    mot = 0
    motionFile = "var/motion"

    approvalNeeded = 5 # How many "yes/no" is needed to pass/fail a vote.
    numberOfBots = 2 #2 # DEBUG

    def __init__(self, bot):
        self.bot = bot

        # Load saved motion from file.
        if os.path.isfile(self.motionFile):
            self.mot = pickle.load( open(self.motionFile, "rb") )

        if not os.path.isfile("var/motionsNR.txt"):
            with open("var/motionsNR.txt", "w") as f: 
                f.write("0")

        if not os.path.isfile("var/motions.txt"): 
            with open("var/motions.txt", "w") as f: 
                f.write("")

        # Use different values if it's running with dev code.
        try:
            if config.gitDev:
                self.approvalNeeded = 1 # How many "yes" is needed to pass a vote.
                self.numberOfBots = 1 #2 # DEBUG
        except:
            pass

        # Check for folder, add if it doesn't exist.
        directory = os.path.dirname("var/")
        try:
            os.stat(directory)
        except:
            os.mkdir(directory) 

    @commands.group(pass_context=True)
    async def motion(self, ctx):
        """View current motion or create a new one."""
        if ctx.invoked_subcommand is None:
            await self.motionHandler()
            

    @motion.command(pass_context=True)
    async def new(self, ctx, *, motion : str):
        """Create a new motion."""
        if self.mot == 0:
            self.mot = Motion(newMotion = motion, newProp = ctx.message.author.id)
            pickle.dump( self.mot, open(self.motionFile, "wb") )
            
        # Inform users that new motion started.
        await self.motionHandler()
        

    async def motionHandler(self, edit = False):
        """Motion handler."""
        if self.mot == 0:
            await self.bot.say("No motion in progress.")
        else:
            await self.motionEmbed(edit = edit)

            if edit:
                pickle.dump( self.mot, open(self.motionFile, "wb") )

#            users = int(self.bot.servers[0].member_count) - self.numberOfBots
#            self.approvalNeeded = (users / 2) #+ 1 # DEBUG

            # Checks for approval.
            if len(self.mot.yes) >= self.approvalNeeded:
                # Vote passes
                await self.motionEmbed(edit = True, status = "Passed.") # Edit all previous Embeds
                await self.motionEmbed(edit = False, status = "Passed.") # Create an ending embed.
                await self.resetMotion(passed = True) # Reset the voting.

            # Checks for disapproval.
            elif len(self.mot.no) >= self.approvalNeeded:
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
                msg = "**$" + str(lawNR) + ":** " + self.mot.motion + "\n**Proposal by:** <@" + self.mot.proposalBy + ">\n - Votes: "

                msg += "For: "
                for voter in self.mot.yes:
                    msg += "<@" + voter + ">, "

                msg += " Against: "
                for voter in self.mot.no:
                    msg += "<@" + voter + ">, "

                msg += " Abstain: "
                for voter in self.mot.abs:
                    msg += "<@" + voter + ">, "

                file.write(msg + "\n\n")


        # Clear the motion.
        self.mot = 0
        os.remove(self.motionFile)



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

            if voter in self.mot.yes:
                self.mot.yes.remove(voter)
            elif voter in self.mot.no:
                self.mot.no.remove(voter)
            elif voter in self.mot.abs:
                self.mot.abs.remove(voter)
            
            if ballot == "yay":
                self.mot.yes.append(voter)
                await self.bot.add_reaction(ctx.message, "\U00002705") # Yes

            elif ballot == "nay":
                self.mot.no.append(voter)
                await self.bot.add_reaction(ctx.message, "\U0000274E") # No

            elif ballot == "abstain":
                self.mot.abs.append(voter)
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