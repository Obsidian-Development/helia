import discord
import asyncio
import os
from discord.ext import commands


class submits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def sub(self, ctx):
        subinfo = discord.Embed(title="Command sub", description="Used to create a vote, proposal.. ",
                                color=0x00ff00)
        subinfo.add_field(name="Usage", value="``sub create``- create suggestion. ", inline=True)
        await ctx.send(embed=subinfo)

    @sub.command(pass_context=True)
    async def create(self, ctx, *, arg):
        author = ctx.message.author
        subtxt = os.path.join(r"db/submits/", f"submit_{author.guild.id}.txt")
        if author.guild_permissions.manage_messages:
            with open(subtxt, "r") as file:
                subset = file.read()
                chan = int(subset)
            channel = self.bot.get_channel(chan)
            user = ctx.message.author
            submit = discord.Embed(title=f"<:speech_balloon:644199603033473055> User suggestion {user}",
                                   description=arg, color=0x00ff00)
            msg = await channel.send(embed=submit)
            emoj = self.bot.get_emoji(656155011687907358)
            emoj2 = self.bot.get_emoji(656155011746889758)
            await msg.add_reaction(emoj)
            await msg.add_reaction(emoj2)
        else:
            await ctx.send(
                "bot: Insufficient permissions to execute this command. Necessary Rights: **Manage Messages**")

    @sub.command(pass_context=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        author = ctx.message.author
        subtxt = os.path.join(f"db/submits/submit_{author.guild.id}.txt")
        if author.guild_permissions.administrator:
            if os.path.exists(subtxt):
                os.remove(subtxt)
            with open(subtxt, "a") as sub_f:
                sub_f.write(f"{channel.id}")
            await ctx.send(f"bot: Channel for bot suggestions was set to  {channel.mention}")
        else:
            await ctx.send("bot: Insufficient permissions to execute this command. Necessary rights: ** Administrator **")

    @sub.command(pass_context=True)
    async def clear(self, ctx):
        author = ctx.message.author
        if author.guild_permissions.administrator:
            sclear = os.path.join(f"db/submits/submit_{author.guild.id}.txt")
            if os.path.exists(sclear):
                os.remove(sclear)
            await ctx.send("bot: Config File Cleared")
        else:
            await ctx.send("bot: Insufficient permissions to execute this command. Necessary rights: ** Administrator **")





def setup(bot):
    bot.add_cog(submits(bot))