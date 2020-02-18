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
            return await ctx.send("blacklist-warn: Please Dont use everyone or here")
        else:    
            return await ctx.send(content)

    @commands.command(pass_context=True , aliases=['name', 'set_name', 'prozvische'])
    async def setname(self, ctx, member: discord.Member, *, nickname=None):
       try:
          '''
          Change user's nickname
          '''
          await member.edit(nick=nickname)
          await ctx.message.delete()
          embed=discord.Embed(title="Name set", color=0xff8000)
          await ctx.send(embed=embed)  
          
       except discord.errors.Forbidden:
          embed=discord.Embed(title="🔴 Error", description="I need the ``Manage Nicknames`` permission to do this.", color=0xdd2e44,)
          await ctx.send(embed=embed)
          
            
   










def setup(bot):
    bot.add_cog(fun(bot))

