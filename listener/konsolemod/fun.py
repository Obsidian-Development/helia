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
    async def barany(self, ctx):
        embed=discord.Embed(title="Песня Про Путина И Баранов ")
        embed.add_field(name="1", value="на российской на земле путин пас барана путин скот держал в говне как ублюдков сраных.", inline=False)
        embed.add_field(name="2", value="но бараны дураки путина любили и за вовой дружно шли блея голосили", inline=False)
        embed.add_field(name="3", value="путину слава так нам и надо да здравствует путин мы же не люди", inline=False)
        embed.add_field(name="4", value="путин часто обещал накормить барана и отмыть их от говна поздно или рано", inline=False)
        embed.add_field(name="5", value="и бараны дураки на него молились и за вовой дружно шли блея голосили путину слава", inline=False)
        embed.add_field(name="6", value="так нам и надо да здравствует путин мы же не люди путину слава", inline=False)
        embed.add_field(name="7", value="так нам и надо да здравствует путин мы же не люди этот гребаный пастух пас давно россию", inline=False)
        embed.add_field(name="8", value="и баранам дуракам чудился мессия и бараны дураки путина любили и за вовой дружно шли блея голосили", inline=False)
        embed.add_field(name="9", value="путину слава так нам и надо да здравствует путин мы же не люди", inline=False)
        embed.add_field(name="10", value="путину слава так нам и надо да здравствует путин мы же не люди", inline=False)
        embed.add_field(name="11", value="смысл у песни очень прост и понятен многим что в россии как всегда дураки к дороге а дорог в россии нет", inline=False)
        embed.add_field(name="12", value="есть бараны-люди и такими дураками будет править путин путину слава так нам и надо", inline=False)
        embed.add_field(name="13", value="да здравствует путин мы же не люди путину слава так нам и надо да здравствует путин мы же не люди", inline=False)
        embed.add_field(name="_____", value="____", inline=True)
        await ctx.send(embed=embed)








def setup(bot):
    bot.add_cog(fun(bot))

