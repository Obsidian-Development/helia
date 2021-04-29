# -*- coding: utf-8 -*-

from typing import NoReturn

from discord.ext import commands
from discord.ext.commands import Bot, Context

from cogs.utils import Logger, Settings, Config, Strings, Utils


CONFIG = Config()


class Other(commands.Cog, name='Other'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Other'

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx: Context) -> NoReturn:
        """Shows host latency.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        latency = int(round(self.bot.latency * 100, 1))

        embed = Utils.done_embed(
            STRINGS['other']['pong'].format(str(latency)))
        await ctx.send(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Other(bot))
    Logger.cog_loaded(bot.get_cog('Other').name)
