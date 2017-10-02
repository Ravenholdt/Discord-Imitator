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

        self.status = "in Progress."

        # Ballot
        self.yes = []
        self.no = []
        self.abs = []

        # List of all Motion embeds for editing.
        self.lastMsg = []

        self.id = int(self.proposalBy) % len(self.motion)


class Democracy:
    
    mot = []
    maxMotion = 3
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
        if len(self.mot) < self.maxMotion:
            
            newMotion = Motion(newMotion = motion, newProp = ctx.message.author.id)
            
            idPass = False
            while not idPass:
                for motions in self.mot:
                    if motions.id == newMotion.id:
                        newMotion.id += 1
                        idPass = False
                idPass = True

            self.mot.append(newMotion)
            pickle.dump( self.mot, open(self.motionFile, "wb") )
            
            # Inform users that new motion started.
            await self.motionHandler()
        
        else:
            await self.bot.say("Too many motions in progress.")
        

    async def motionHandler(self, edit = False, motion = 0):
        """Motion handler."""
        if len(self.mot) == 0:
            await self.bot.say("No motions in progress.")
        else:
            await self.motionEmbed(edit = edit, motion = motion)

            if edit:
                pickle.dump( self.mot, open(self.motionFile, "wb") )

#            users = int(self.bot.servers[0].member_count) - self.numberOfBots
#            self.approvalNeeded = (users / 2) #+ 1 # DEBUG

            # Checks for approval.
            for motions in self.mot:
                if len(motions.yes) >= self.approvalNeeded:
                    # Vote passes
                    motions.status = "Passed."

                    await self.motionEmbed(edit = True, motion = motions) # Edit all previous Embeds
                    await self.motionEmbed(edit = False, motion = motions) # Create an ending embed.
                    await self.resetMotion(motion = motions, passed = True) # Reset the voting.

                # Checks for disapproval.
                elif len(motions.no) >= self.approvalNeeded:
                    # Vote failed
                    motions.status = "Failed."

                    await self.motionEmbed(edit = True, motion = motions) # Edit all previous Embeds
                    await self.motionEmbed(edit = False, motion = motions) # Create an ending embed.
                    await self.resetMotion(motion = motions, passed = False) # Reset the voting.


    async def motionEmbed(self, edit = False, motion = 0):
        """Motion display."""

        motions = [motion]

        if motion == 0:
            motions = self.mot

        for motion in motions:
            
            # Create the embed
            embTitle = "Motion #" + str(motion.id) + " " + motion.status
            embed=discord.Embed(title=embTitle)
            embed.add_field(name="------------------", value=motion.motion, inline=False)

            value = "\U00002705 " + str(len(motion.yes)) + "  |  \U0000274E " + str(len(motion.no)) + "  |  \U00002611 " + str(len(motion.abs))
            embed.add_field(name="Votes", value=value, inline=True)
            embed.set_footer(text= "Proposal by: <@" + motion.proposalBy + ">  " + str(motion.date))

            if edit: # Update already existing embed
                for motionMsg in motion.lastMsg:
                        await self.bot.edit_message(motionMsg, embed=embed)
            else: # Create a new embed
                motMsg = await self.bot.say(embed=embed)
                motion.lastMsg.append(motMsg)
                

    async def resetMotion(self, motion, passed = False):
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
                msg = "**$" + str(lawNR) + ":** " + motion.motion + "\n**Proposal by:** <@" + motion.proposalBy + ">\n - Votes: "

                msg += "For: "
                for voter in motion.yes:
                    msg += "<@" + voter + ">, "

                msg += " Against: "
                for voter in motion.no:
                    msg += "<@" + voter + ">, "

                msg += " Abstain: "
                for voter in motion.abs:
                    msg += "<@" + voter + ">, "

                file.write(msg + "\n\n")


        # Clear the motion.
        self.mot.remove(motion)
        pickle.dump( self.mot, open(self.motionFile, "wb") )



    @commands.group(pass_context=True)
    async def vote(self, ctx):
        """Vote!"""

    @vote.command(pass_context=True)
    async def yay(self, ctx, motionID : int):
        """Vote yes!"""
        await self.votingHandler(ctx, "yay", motionID)

    @vote.command(pass_context=True)
    async def nay(self, ctx, motionID : int):
        """Vote no!"""
        await self.votingHandler(ctx, "nay", motionID)

    @vote.command(pass_context=True)
    async def abstain(self, ctx, motionID : int):
        """Beggars can't be choosers."""
        await self.votingHandler(ctx, "abstain", motionID)


    async def votingHandler(self, ctx, ballot : str, motionID):
        """Voting handler."""
        if len(self.mot) > 0:
            voter = ctx.message.author.id # Get id of the voter

            for motions in self.mot:
                if motions.id == motionID:
                    if voter in motions.yes:
                        motions.yes.remove(voter)
                    elif voter in motions.no:
                        motions.no.remove(voter)
                    elif voter in motions.abs:
                        motions.abs.remove(voter)
                    
                    if ballot == "yay":
                        motions.yes.append(voter)
                        await self.bot.add_reaction(ctx.message, "\U00002705") # Yes

                    elif ballot == "nay":
                        motions.no.append(voter)
                        await self.bot.add_reaction(ctx.message, "\U0000274E") # No

                    elif ballot == "abstain":
                        motions.abs.append(voter)
                        await self.bot.add_reaction(ctx.message, "\U00002611") # Abstain

                    await self.motionHandler(edit = True, motion = motions)


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