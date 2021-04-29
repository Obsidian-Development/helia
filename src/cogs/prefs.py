# -*- coding: utf-8 -*-

from typing import NoReturn

from discord.ext import commands
from discord.ext.commands import Bot, Context

from cogs.utils import Logger, Settings, Config, Strings, Utils


CONFIG = Config()


class Prefs(commands.Cog, name='Prefs'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Prefs'

    @commands.command(aliases=['setprefix'])
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
        await s.set_field('prefix', prefix)

        await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.command(aliases=['lang', 'setlang', 'language'])
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
        locales = Utils.get_locales_list()

        for _locale in locales:
            if _locale == locale:
                await s.set_field('locale', locale)

                await ctx.message.add_reaction(CONFIG['yes_emoji'])
                return

        # FIXME
        await ctx.send("нет такой локали какбы")


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Prefs(bot))
    Logger.cog_loaded(bot.get_cog('Prefs').name)
