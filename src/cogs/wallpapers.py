import asyncio
import random

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from cogs.utils import Config, Logger, Settings, Strings
from scripts import desAnime, desNature, desStarwars

CONFIG = Config()


class wallpapers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def wallpaper(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        wallinfo = discord.Embed(
            title=STRINGS["wallpaper"]["wallpaperembedtitle"],
            description=STRINGS["wallpaper"]["wallpaperdesc"],
            color=0x00FF00,
        )
        wallinfo.add_field(
            name=STRINGS["wallpaper"]["wallpaperusageanimetitle"],
            value="``wallpaper anime``",
            inline=True,
        )
        wallinfo.add_field(
            name=STRINGS["wallpaper"]["wallpaperusagenaturetitle"],
            value="``wallpaper nature``",
            inline=True,
        )
        wallinfo.add_field(
            name=STRINGS["wallpaper"]["wallpaperusagestarwarstitle"],
            value="``wallpaper starwars``",
            inline=True,
        )
        await ctx.send(embed=wallinfo)

    @wallpaper.command()
    async def anime(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        embedanime = discord.Embed(
            title=STRINGS["wallpaper"]["wallpaperanimetitle"],
            color=0x00FF00,
        )
        embedanime.set_footer(text=STRINGS["wallpaper"]["wallpaperanimefooter"])
        await ctx.send(embed=embedanime)

    @wallpaper.command()
    async def nature(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        imgnat = random.choice(desNature.images)
        embednat = discord.Embed(
            title=STRINGS["wallpaper"]["wallpapernaturetitle"],
            color=0x00FF00,
            url=imgnat,
        )
        embednat.set_image(url=imgnat)
        await ctx.send(embed=embednat)

    @wallpaper.command()
    async def starwars(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        imgstarwars = random.choice(desStarwars.images)
        embedstarwars = discord.Embed(
            title=STRINGS["wallpaper"]["wallpaperstarwarstitle"],
            color=0x00FF00,
            url=imgstarwars,
        )
        embedstarwars.set_image(url=imgstarwars)
        await ctx.send(embed=embedstarwars)


def setup(client):
    client.add_cog(wallpapers(client))
