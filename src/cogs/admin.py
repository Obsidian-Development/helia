# -*- coding: utf-8 -*-
import asyncio
import datetime
from os.path import abspath, dirname
from typing import NoReturn

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord_components import Button, ButtonStyle, DiscordComponents, InteractionType
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
            "353049432037523467",
        ]
        select_components = [
            [
                Button(style=ButtonStyle.green, label="✓"),
                Button(style=ButtonStyle.red, label="X"),
            ]
        ]
        done_components = [
            [
                Button(style=ButtonStyle.grey, label="·", disabled=True),
            ]
        ]

        embedconfirm = discord.Embed(
            title=STRINGS["moderation"]["shutdownembedtitle"],
            description=STRINGS["moderation"]["shutdownconfirm"],
        )
        await ctx.send(embed=embedconfirm, components=select_components)
        response = await self.bot.wait_for(
            "button_click", check=lambda message: message.author == ctx.author
        )
        if str(author.id) in valid_users and response.component.label == "✓":
            await response.respond(
                type=7,
                embed=discord.Embed(
                    title=STRINGS["moderation"]["shutdownembedtitle"],
                    description=STRINGS["moderation"]["shutdownembeddesc"],
                    color=0xFF8000,
                ),
                components=done_components,
            )

            await ctx.bot.change_presence(
                activity=discord.Game(name="Shutting down for either reboot or update ")
            )
            await asyncio.sleep(5)
            print("---------------------------")
            print("[SHUTDOWN] Shutdown requested by bot owner")
            print("---------------------------")
            await ctx.bot.close()
        else:
            await response.respond(
                type=7,
                embed=discord.Embed(
                    title=STRINGS["moderation"]["shutdownaborttitle"],
                    description=STRINGS["moderation"]["shutdownabortdesc"],
                    color=0xDD2E44,
                ),
                components=done_components,
            )

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
        menu_components = [
            [
                Button(
                    style=ButtonStyle.URL,
                    label=STRINGS["general"]["botinvitetitle"],
                    url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=204859462&scope=applications.commands%20bot",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label=STRINGS["general"]["botinvitedescd"],
                    url=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=204557314",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label=STRINGS["general"]["canaryver"],
                    url=f"https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label=STRINGS["general"]["botupsdc"],
                    url=f"https://bots.server-discord.com/{self.bot.user.id}",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label=STRINGS["general"]["botuptopgg"],
                    url=f"https://top.gg/bot/{self.bot.user.id}",
                ),
                # Button(style=ButtonStyle.URL, label=STRINGS["general"]["botupbod"], url=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}"),
                # Button(style=ButtonStyle.URL, label=STRINGS["general"]["botupdblco"], url=f"https://discordbotslist.co/bot/{self.bot.user.id}"),
            ]
        ]
        menuer_components = [
            [
                Button(
                    style=ButtonStyle.URL,
                    label=STRINGS["general"]["botupbod"],
                    url=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label=STRINGS["general"]["botupdblco"],
                    url=f"https://discordbotslist.co/bot/{self.bot.user.id}",
                ),
            ]
        ]

        embed = discord.Embed(
            title=STRINGS["general"]["invitedescd"],
            colour=discord.Colour(0xFF6900),
            # url=
            # f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=204859462&scope=applications.commands%20bot",
            description=STRINGS["general"]["botinvitedesc"],
        )
        # embed.set_author(
        # name=STRINGS["general"]["botinvitedescd"],
        # url=
        # f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=204557314",
        # )
        # mostly useful for helia canary invite but still why not have it be there - comment if your self hosted version will not have canary branch
        # embed.add_field(
        # name=STRINGS["general"]["canaryver"],
        # value=
        # f"https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",
        # inline=False,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupsdc"],
        # value=f"https://bots.server-discord.com/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botuptopgg"],
        # value=f"https://top.gg/bot/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupbod"],
        # value=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupdblco"],
        # value=f"https://discordbotslist.co/bot/{self.bot.user.id}",
        # inline=True,
        # )
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        embedcont = discord.Embed(title="-----", colour=discord.Colour(0xFF6900))
        await ctx.send(embed=embed, components=menu_components)
        await ctx.send("`----`", components=menuer_components)
      
    @commands.command(brief = "Gives the bot's uptime")
    async def uptime(self, ctx):
         delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
         hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
         minutes, seconds = divmod(remainder, 60)
         days, hours = divmod(hours, 24)
         embed=discord.Embed(title="Bot uptime")
         embed.add_field(name="Days", value=f"```{days}d```", inline=True)
         embed.add_field(name="Hours", value=f"```{hours}h```", inline=True)
         embed.add_field(name="Minutes", value=f"```{minutes}m```", inline=False)
         embed.add_field(name="Seconds", value=f"```{seconds}s```", inline=False)
         await ctx.send(embed=embed)
      
    # @commands.command()
    # @commands.is_owner()
    # async def guildlist(self, ctx: SlashContext, bot : Bot):
    # await ctx.send(bot.guilds)


def setup(bot: Bot) -> NoReturn:
    DiscordComponents(bot)
    bot.add_cog(Admin(bot))
    Logger.cog_loaded(bot.get_cog("Admin").name)
