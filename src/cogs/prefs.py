# -*- coding: utf-8 -*-
from typing import NoReturn

import discord
from cogs.utils import Config
from cogs.utils import Logger
from cogs.utils import Settings
from cogs.utils import Strings
from cogs.utils import Utils
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

CONFIG = Config()


class Prefs(commands.Cog, name="Prefs"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Prefs"

    @commands.command(aliases=["setprefix"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx: Context, prefix: str) -> NoReturn:
        """Sets a custom prefix.

        Attributes:
        -----------
        - `prefix` - new prefix

        """
        s = await Settings(ctx.guild.id)
        await s.set_field("prefix", prefix)

        await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(aliases=["lang", "setlang", "language"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def locale(self, ctx: Context, locale: str) -> NoReturn:
        """Sets bot language. If not found, it throws an error.

        Attributes:
        -----------
        - `locale` - new locale

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        locales = Utils.get_locales_list()

        for _locale in locales:
            if _locale == locale:
                await s.set_field("locale", locale)

                await ctx.message.add_reaction(CONFIG["yes_emoji"])
                return

        # FIXME
        embed = discord.Embed(
            title=STRINGS["error"]["on_error_title"],
            description=STRINGS["error"]["localeerrortext"],
            color=0xFF0000,
        )
        embed.add_field(
            name=STRINGS["error"]["generictracebackthing"],
            value=STRINGS["error"]["localerrrorstring"],
            inline=False,
        )
        print(f"Wrong localization given on {ctx.message.guild}")
        await ctx.send(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Prefs(bot))
    Logger.cog_loaded(bot.get_cog("Prefs").name)
