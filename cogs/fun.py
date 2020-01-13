import discord
import asyncio
from discord.ext import commands

class fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def echo(self, ctx,*, arg):
       # await ctx.send(arg)
       await ctx.send("bot: The Command Is Currently Disabled")


    @commands.command()
    async def ping(self, ctx):
        for pings in range(4):
            await ctx.send("bot: Ping , Pong")









def setup(bot):
    bot.add_cog(fun(bot))

