# -*- coding: utf-8 -*-
import asyncio
from os.path import abspath, dirname
from typing import NoReturn

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord_slash import SlashContext, cog_ext

from cogs.utils import Config, Logger, Settings, Strings, Utils

CONFIG = Config()
STRINGS = Strings(CONFIG["default_locale"])


class Admin(commands.Cog, name="Admin"):
    """A module required to administer the bot. Only works for its owners."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Admin"

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.load_extension(f"cogs.{module}")
        except Exception as e:
            await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: Context, *, module: str) -> NoReturn:
        """Unloads a module (cog). If the module is not found, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.unload_extension(f"cogs.{module}")
        except Exception as e:
            await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:

            await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(name="reload")
    @commands.is_owner()
    async def _reload(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.reload_extension(f"cogs.{module}")
        except Exception as e:
            await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(description="Bot restart/shutdown")
    async def shutdown(self, ctx: SlashContext):  # Команда для выключения бота
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = ctx.message.author
        valid_users = [
            "540142383270985738",
            "573123021598883850",
            "584377789969596416",
            "106451437839499264",
            "237984877604110336",
            "579750505736044574",
            "497406228364787717",
        ]
        if str(author.id) in valid_users:
            embed = discord.Embed(
                title=STRINGS["moderation"]["shutdownembedtitle"],
                description=STRINGS["moderation"]["shutdownembeddesc"],
                color=0xFF8000,
            )
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            await ctx.bot.change_presence(
                activity=discord.Game(name="Shutting down for either reboot or update ")
            )
            await asyncio.sleep(5)
            print("---------------------------")
            print("[SHUTDOWN] Shutdown requested by bot owner")
            print("---------------------------")
            await ctx.bot.close()
        else:
            embed2 = discord.Embed(
                title="🔴 Error",
                description="You need the ``Bot Owner`` permission to do this.",
                color=0xDD2E44,
            )
            await ctx.send(embed=embed2)

    @commands.command(description="Set bot status")
    async def set_status(self, ctx, *args):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = ctx.message.author
        valid_users = [
            "540142383270985738",
            "573123021598883850",
            "584377789969596416",
            "106451437839499264",
            "237984877604110336",
            "579750505736044574",
            "497406228364787717",
        ]
        if str(author.id) in valid_users:
            await self.bot.change_presence(activity=discord.Game(" ".join(args)))
            embed = discord.Embed(
                title=STRINGS["moderation"]["setstatustext"],
                description=STRINGS["moderation"]["setstatusdesc"],
                color=0xFF8000,
            )
            embed.add_field(
                name=STRINGS["moderation"]["setstatusfieldtext"],
                value=STRINGS["moderation"]["setstatusfielddesc"],
                inline=True,
            )
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        else:
            embed = discord.Embed(
                title="You failed",
                description="Need Permission : Bot Owner",
                color=0xFF0000,
            )

        await ctx.send(embed=embed)

    @commands.command(description="Bot invite links")
    async def invite(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        embed = discord.Embed(
            title=STRINGS["general"]["botinvitetitle"],
            colour=discord.Colour(0xFF6900),
            url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=204859462&scope=applications.commands%20bot",
            description=STRINGS["general"]["botinvitedesc"],
        )
        embed.set_author(
            name=STRINGS["general"]["botinvitedescd"],
            url=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=204557314",
        )
        # mostly useful for helia canary invite but still why not have it be there - comment if your self hosted version will not have canary branch
        embed.add_field(
            name=STRINGS["general"]["canaryver"],
            value=f"https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",
            inline=False,
        )
        embed.add_field(
            name=STRINGS["general"]["botupsdc"],
            value=f"https://bots.server-discord.com/{self.bot.user.id}",
            inline=True,
        )
        embed.add_field(
            name=STRINGS["general"]["botuptopgg"],
            value=f"https://top.gg/bot/{self.bot.user.id}",
            inline=True,
        )
        embed.add_field(
            name=STRINGS["general"]["botupbod"],
            value=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}",
            inline=True,
        )
        embed.add_field(
            name=STRINGS["general"]["botupdblco"],
            value=f"https://discordbotslist.co/bot/{self.bot.user.id}",
            inline=True,
        )
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    # @commands.command()
    # @commands.is_owner()
    # async def guildlist(self, ctx: SlashContext, bot : Bot):
    # await ctx.send(bot.guilds)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Admin(bot))
    Logger.cog_loaded(bot.get_cog("Admin").name)
