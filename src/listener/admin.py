# -*- coding: utf-8 -*-
import asyncio
import datetime
import os
import typing
from os import system as sys
from os.path import abspath, dirname
from typing import NoReturn

import discord
from discord import ButtonStyle, SelectOption
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord.ui import Button, Select, View
from dotenv import load_dotenv

from listener.utils import Config, Logger, Settings, Strings, Utils

# from discord_components import Button, ButtonStyle, discordComponents

# from discord.ext.commands import Bot, Context

CONFIG = Config()
# STRINGS = Strings(CONFIG["default_locale"])


class Confirm(discord.ui.View):
    def __init__(self, ctx, bot: Bot):
        super().__init__()
        self.bot = bot
        self.ctx = ctx
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(style=ButtonStyle.green, label="✓", custom_id="yes")
    async def confirm(self, button: discord.ui.Button,
                      interaction: discord.Interaction):
        s = await Settings(self.ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = self.ctx.message.author
        valid_users = [
            "540142383270985738",
            "573123021598883850",
            "584377789969596416",
            "106451437839499264",
            "237984877604110336",
            "579750505736044574",
            "497406228364787717",
            "353049432037523467",
            "717822288375971900",
            "168422909482762240",
        ]

        if str(author.id) in valid_users:

            await interaction.response.edit_message(
                embed=discord.Embed(
                    title=STRINGS["moderation"]["shutdownembedtitle"],
                    description=STRINGS["moderation"]["shutdownembeddesc"],
                    color=0xFF8000,
                ),
                view=None,
            )
            await self.bot.change_presence(
                status=discord.Status.online,
                activity=discord.Game(
                    name="Shutting down for either reboot or update "),
            )
            await asyncio.sleep(5)
            print("---------------------------")
            print("[SHUTDOWN] Shutdown requested by bot owner")
            print("---------------------------")
            await self.bot.close()
        else:
            await interaction.response.edit_message(
                embed=discord.Embed(
                    title=STRINGS["moderation"]["shutdownaborttitle"],
                    description=STRINGS["moderation"]["shutdownabortdesc"],
                    color=0xDD2E44,
                ),
                view=None,
            )
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(style=ButtonStyle.red, label="X", custom_id="no")
    async def cancel(self, button: discord.ui.Button,
                     interaction: discord.Interaction):
        s = await Settings(self.ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = self.ctx.message.author
        await interaction.response.edit_message(
            embed=discord.Embed(
                title=STRINGS["moderation"]["shutdownaborttitle"],
                description=STRINGS["moderation"]["shutdownabortdesc"],
                color=0xDD2E44,
            ),
            view=None,
        )
        self.value = False
        self.stop()


class Admin(commands.Cog, name="Admin"):
    """A module required to administer the bot. Only works for its owners."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Admin"

    @commands.command(slash_command=True, message_command=True)
    @commands.is_owner()
    async def load(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.load_extension(f"listener.{module}")
            embeder=discord.Embed(title=f"Module {module} has been loaded", color=0x0c0c0c)
            await ctx.send(embed=embeder,ephemeral=True)
        except Exception as e:
            #await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        #else:
            #await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(slash_command=True, message_command=True)
    @commands.is_owner()
    async def unload(self, ctx: Context, *, module: str) -> NoReturn:
        """Unloads a module (cog). If the module is not found, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.unload_extension(f"listener.{module}")
            embederx=discord.Embed(title=f"Module {module} has been unloaded", color=0x0c0c0c)
            await ctx.send(embed=embederx,ephemeral=True)
        except Exception as e:
            #await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        #else:

            #await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(slash_command=True,
                      message_command=True,
                      name="reload")
    @commands.is_owner()
    async def _reload(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.reload_extension(f"listener.{module}")
            embederxx=discord.Embed(title=f"Module {module} has been reloaded", color=0x0c0c0c)
            await ctx.send(embed=embederxx,ephemeral=True)
        except Exception as e:
            #await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        #else:
            #await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(slash_command=True,
                      message_command=True,
                      name="invite_bot",brief="Makes a bot invite without any permissions")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def invite_bot(self,
                         ctx,
                         *,
                         user: typing.Optional[discord.User] = None):
        user = user or ctx.author

        if not user.bot:
            embed = discord.Embed(
                title="Error",
                description="The provided user id is not a bot!",
                color=0xFF0000,
            )

            return await ctx.send(embed=embed)

        invite = discord.utils.oauth_url(client_id=user.id,
                                         scopes=("bot",
                                                 "applications.commands"))
        embeder = discord.Embed(
            title="Generating invite for the provided user id", color=0x778EFD)
        waiter = await ctx.send(embed=embeder, delete_after=5)
        await asyncio.sleep(5)
        embedtimes = discord.Embed(title="Your invite", color=0x778EFD)
        embedtimes.add_field(name="Is here", value=f"{invite}", inline=True)
        await ctx.send(embed=embedtimes)

    @commands.command(slash_command=True,
                      message_command=True,
                      name="shutdown",description="Bot restart/shutdown")
    async def shutdown(self, ctx: Context):  # Команда для выключения бота
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = ctx.message.author
        viewb = Confirm(ctx, self.bot)
        viewbx = discord.ui.View()
        valid_users = [
            "540142383270985738",
            "573123021598883850",
            "584377789969596416",
            "106451437839499264",
            "237984877604110336",
            "579750505736044574",
            "497406228364787717",
            "353049432037523467",
            "717822288375971900",
            "168422909482762240",
        ]

        viewbx.add_item(
            Button(style=ButtonStyle.grey, label="·", disabled=True))
        embedconfirm = discord.Embed(
            title=STRINGS["moderation"]["shutdownembedtitle"],
            description=STRINGS["moderation"]["shutdownconfirm"],
        )
        await ctx.send(embed=embedconfirm, view=viewb)
        await viewb.wait()

    @commands.command(slash_command=True,
                      message_command=True,description="Set bot status")
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
            await self.bot.change_presence(
                activity=discord.Game(" ".join(args)))
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
            embed.set_footer(text=self.bot.user.name,
                             icon_url=self.bot.user.avatar.url)
        else:
            embed = discord.Embed(
                title="You failed",
                description="Need Permission : Bot Owner",
                color=0xFF0000,
            )

        await ctx.send(embed=embed)

    @commands.command(description="Bot restart")
    @commands.is_owner()
    async def restart(self, ctx):

        for ext in self.bot.cogs:  # Idk how you called it
            self.bot.reload_extension(f"{ext}")

    @commands.command(slash_command=True,
                      message_command=True,description="Bot invite links")
    async def invite(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        view = discord.ui.View()
        viewx = discord.ui.View()
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botinvitetitle"],
                url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=204859462&scope=applications.commands%20bot",
            ))
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botinvitedescd"],
                url=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=204557314",
            ))
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["canaryver"],
                url="https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",
            ))
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupsdc"],
                url=f"https://bots.server-discord.com/{self.bot.user.id}",
            ))
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botuptopgg"],
                url=f"https://top.gg/bot/{self.bot.user.id}",
            ))
        viewx.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupbod"],
                url=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}",
            ))
        viewx.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupdblco"],
                url=f"https://discordbotslist.co/bot/{self.bot.user.id}",
            ))
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
        embed.set_footer(text=self.bot.user.name,
                         icon_url=self.bot.user.avatar.url)

        embedcont = discord.Embed(title="-----",
                                  colour=discord.Colour(0xFF6900))
        await ctx.send(embed=embed, view=view)
        await ctx.send("`----`", view=viewx)

    @commands.command(slash_command=True,
                      message_command=True,brief="Gives the bot's uptime")
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(title="Bot uptime")
        embed.add_field(name="Days", value=f"```{days}d```", inline=True)
        embed.add_field(name="Hours", value=f"```{hours}h```", inline=True)
        embed.add_field(name="Minutes",
                        value=f"```{minutes}m```",
                        inline=False)
        embed.add_field(name="Seconds",
                        value=f"```{seconds}s```",
                        inline=False)
        await ctx.send(embed=embed)

    # @commands.command()
    # @commands.is_owner()
    # async def guildlist(self, ctx: Context, bot : Bot):
    # await ctx.send(bot.guilds)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Admin(bot))
    Logger.cog_loaded(bot.get_cog("Admin").name)
