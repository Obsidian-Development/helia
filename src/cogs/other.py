# -*- coding: utf-8 -*-
from typing import NoReturn

from cogs.utils import Config
from cogs.utils import Logger
from cogs.utils import Settings
from cogs.utils import Strings
from cogs.utils import Utils
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

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


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Other(bot))
    Logger.cog_loaded(bot.get_cog("Other").name)
