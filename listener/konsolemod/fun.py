import discord
import asyncio
from discord.ext import commands
from scripts import blacklist

class fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, content):
        if blacklist.list in content:
            return await ctx.send("Please Dont use everyone or here")
        else:    
            return await ctx.send(content)

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

