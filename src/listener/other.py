# -*- coding: utf-8 -*-
from typing import NoReturn

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings, Utils
from scripts import desAnime, desNature, desStarwars

CONFIG = Config()


class Other(commands.Cog, name="Other"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Other"

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx: Context) -> NoReturn:
        """Shows host latency."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        latency = int(round(self.bot.latency * 100, 1))

        embed = Utils.done_embed(STRINGS["other"]["pong"].format(str(latency)))
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def wallpaper(self, ctx: Context):
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
    async def anime(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        embedanime = discord.Embed(
            title=STRINGS["wallpaper"]["wallpaperanimetitle"],
            color=0x00FF00,
        )
        embedanime.set_footer(
            text=STRINGS["wallpaper"]["wallpaperanimefooter"])
        await ctx.send(embed=embedanime)

    @wallpaper.command()
    async def nature(self, ctx: Context):
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
    async def starwars(self, ctx: Context):
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


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Other(bot))
    Logger.cog_loaded(bot.get_cog("Other").name)
