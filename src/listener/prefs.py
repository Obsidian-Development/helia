# -*- coding: utf-8 -*-
from typing import NoReturn

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings, Utils

CONFIG = Config()


class Preferences(commands.Cog, name="Preferences"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = "Preferences"
        # self.server_prefixes = server_prefixes

    @commands.command(slash_command=True, message_command=True,aliases=["setprefix"])
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
        embederx=discord.Embed(title=f"Prefix has been set to {prefix}", color=0x0c0c0c)
        await ctx.send(embed=embederx,ephemeral=True)

        #await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(slash_command=True, message_command=True,aliases=["lang", "setlang", "language"])
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
                embederx=discord.Embed(title=f"Locale succesfully set!", color=0x0c0c0c)
                await ctx.send(embed=embederx,ephemeral=True)

                #await ctx.message.add_reaction(CONFIG["yes_emoji"])
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
    bot.add_cog(Preferences(bot))
    Logger.cog_loaded(bot.get_cog("Preferences").name)
