import discord
import asyncio
import random
import math
from scripts import blacklist
from discord.ext import commands


class tools(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def randint(self,ctx, stc1:int, stc2:int):
        result = random.randint(stc1, stc2)
        await ctx.send(f"Randome number geneation between {stc1} and {stc2} equals ``{result}``")
 
    @commands.command()
    async def sqrt(self, ctx, num:int):
        result = math.sqrt(num)
        await ctx.send(f"Square root of {num} equals ``{result}``")

    @commands.command()
    async def embed(self,ctx, name,*, content):
        creator = discord.Embed(title=name, description=content)
        await ctx.send(embed = creator)

    @commands.group(invoke_without_command=True)
    async def remind(self, ctx):
        rinfo = discord.Embed(title="Reminder Command", description="Used to create a reminder. Time is indicated in seconds.", color=0x00ff00)
        rinfo.add_field(name="Usage", value="``remind role [Role] [Time]`` - reminder for role \n ``remind me [Time] [Message]`` - reminder for you", inline=True)
        await ctx.send(embed=rinfo)

    @remind.command()
    async def me(self,ctx, time:int,*, content):
        author = ctx.message.author
        if blacklist.list in content:
            await ctx.send("bot: Not enough rights to use this text in a reminder")
        else:
            await ctx.send(f"bot: Reminder successfully installed, off in {time} seconds")
            await asyncio.sleep(time)
            await ctx.send(f"<:alarm_clock:664007109188255745> **Reminder for {author.mention} :** {content}")

    @remind.command()
    async def role(self,ctx,role:discord.Role, time:int,*, content):
        if blacklist.list in content:
            await ctx.send("bot: Not enough rights to use this text in a reminder")
        else:
            if role.mentionable == True:
                await ctx.send(f"bot: Reminder successfully installed, off in {time} seconds")
                await asyncio.sleep(time)
                await ctx.send(f"<:alarm_clock:664007109188255745> **Reminder for {role.mention} :** {content}")
            else:
                await ctx.send("bot: Not Enough Permissions , Mention another role ")


def setup(client):
    client.add_cog(tools(client))
