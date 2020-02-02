import discord
import asyncio
from discord.ext import commands

class fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, content:str):
        if "@everyone" in ctx.message.content:
            return await ctx.send("Don't ping 'everyone' please")
        if "@here" in ctx.message.content:
            return await ctx.send("Don't ping 'here' please")
        await ctx.send(content)

    @commands.command(pass_context=True)
    async def setname(self, ctx, member: discord.Member, *, nickname=None):
       '''
       Change user's nickname
       '''
       if member is ctx.message.author:
            return await ctx.send("Invalid user")
       await member.edit(nick=nickname)
       await ctx.message.delete()
   










def setup(bot):
    bot.add_cog(fun(bot))

