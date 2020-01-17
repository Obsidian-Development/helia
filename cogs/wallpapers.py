import discord
import asyncio
import random
from scripts import desAnime
from scripts import desNature
from discord.ext import commands

class wallpapers(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.group(invoke_without_command=True)
    async def wallpaper(self, ctx):    
        wallinfo = discord.Embed(title="Команда wallpaper", description="Используется для просмотра обоев рабочего стола. ", color=0x00ff00)
        wallinfo.add_field(name="Использование", value="``wallpaper anime`` - for weaboo stupid fucks. \n``wallpaper nature``- nature wallpapers.", inline=True)
        await ctx.send(embed=wallinfo)

    @wallpaper.command()
    async def anime(self, ctx):
        embedanime = discord.Embed(title="Fuck you weaboo", color=0x00ff00, )
        embedanime.set_footer(text="No anime here")
        await ctx.send(embed=embedanime)

    @wallpaper.command()
    async def nature(self, ctx):
        imgnat = random.choice(desNature.images)
        embednat = discord.Embed(title="Nature Wallpapers", color=0x00ff00, url=imgnat)
        embednat.set_image(url=imgnat)
        await ctx.send(embed=embednat)
    
    @wallpaper.command()
    async def starwars(self, ctx):
        imgstarwars = random.choice(desStarwars.images)
        embedstarwars = discord.Embed(title="Star Wars Wallpapers", color=0x00ff00, url=imgstarwars)
        embedstarwars.set_image(url=imgstarwars)
        await ctx.send(embed=embedstarwars)


def setup(bot):
    bot.add_cog(wallpapers(bot))
