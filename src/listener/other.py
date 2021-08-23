# -*- coding: utf-8 -*-
import random
from typing import NoReturn

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings, Utils
from scripts import desAnime, desNature, desStarwars
import asyncio
import functools
import os
import sqlite3

from scripts import db

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
    
    @commands.Cog.listener()
    async def on_member_join(self, member):

        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(
            db.select_table("welcome", "channel_id", "guild_id",
                            member.guild.id))
        chan = cursor.fetchone()
        # print(f" Channel id fetch - {chan[0]}")
        if chan is None:
            return

        cursor.execute(
            db.select_table("welcome", "text", "guild_id", member.guild.id))
        desc = cursor.fetchone()
        hello = discord.Embed(
            title="User joined the server",
            description=f"```Welcome {member} to {member.guild}```",
        )
        hello.set_author(name="Welcome System")
        if desc is None:
            descdef = "Give them a warm welcome and say hello to them"

            hello.add_field(name="Server message",
                            value=f"```{descdef}```",
                            inline=True)
        else:
            hello.add_field(name="Server message",
                            value=f"```{desc[0]}```",
                            inline=True)

        channel = self.bot.get_channel(id=int(chan[0]))
        await channel.send(embed=hello)
        cursor.close()
        connect.close()

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx: Context):
        await ctx.send("No help information temporarily")

    @welcome.command(pass_context=True)
    async def channel(self, ctx: Context, chan: discord.TextChannel = None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "channel_id", "guild_id",
                                    ctx.message.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, chan.id)
                    cursor.execute(
                        db.insert_table("welcome", "guild_id", "channel_id"),
                        val)
                else:
                    cursor.execute(
                        db.update_table(
                            "welcome",
                            "channel_id",
                            chan.id,
                            "guild_id",
                            ctx.message.guild.id,
                        ))
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(
                    f"Set the welcome channel in guild {ctx.message.guild} to {chan.mention} ,the id of it being {chan.id} and id of guild being {ctx.message.guild.id}"
                )
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("Failed to set channel")

    @welcome.command(pass_context=True)
    async def clear(self, ctx: Context):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "channel_id", "guild_id",
                                    ctx.message.guild.id))
                res = cursor.fetchone()
                if res is None:
                    await ctx.send(
                        " Do not have a table for the welcome channel - Check Database."
                    )
                else:
                    cursor.execute(
                        db.delete_table("welcome", "guild_id",
                                        ctx.message.guild.id))
                    await ctx.send(" Cleared the table")
                connect.commit()
                cursor.close()
                connect.close()
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("Failed to remove welcome channel setting")

    @welcome.command(pass_context=True)
    async def text(self, ctx: Context, *, content=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                if content is None:
                    await ctx.send("Setting default message")
                    content = "Give them a warm welcome and say hello to them"
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "text", "guild_id",
                                    ctx.message.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, content)
                    cursor.execute(
                        db.insert_table("welcome", "guild_id", "text"), val)
                else:
                    val = (content, ctx.message.guild.id)
                    cursor.execute(
                        "UPDATE welcome SET text = ? WHERE guild_id = ?", val)
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send("Set the welcome message text")
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("Error , argument may be invalid")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):

        # now  = datetime.now()
        # time = now.strftime("%H:%M:%S")
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(
            db.select_table("goodbye", "channel_id", "guild_id",
                            member.guild.id))
        chan = cursor.fetchone()
        # print(f" Channel id fetch - {chan[0]}")
        if chan is None:
            return
        cursor.execute(
            db.select_table("goodbye", "text", "guild_id", member.guild.id))
        desc = cursor.fetchone()
        descdef = f"The one who left was {member}, who knows his/hers reasons for leaving but we will welcome them with open arms if they return "
        gb = discord.Embed(
            title="User left the server",
            description=f"```Someone left {member.guild}```",
        )
        gb.set_author(name="Goodbye System")


        if desc is None:
            gb.add_field(name="Server message",
                         value=f"{descdef}",
                         inline=True)
        else:
            gb.add_field(name="Server message",
                         value=f"```{desc[0]}```",
                         inline=True)
        channel = self.bot.get_channel(id=int(chan[0]))
        cursor.close()
        connect.close()
        await channel.send(embed=gb)

    @commands.group(invoke_without_command=True)
    async def goodbye(self, ctx: Context):
        await ctx.send("No help information temporarily")

    @goodbye.command()
    async def channel(self, ctx: Context, channel: discord.TextChannel = None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("goodbye", "channel_id", "guild_id",
                                    ctx.message.guild.id))
                result = cursor.fetchone()
                if result is None:
                    val = (ctx.message.guild.id, channel.id)
                    cursor.execute(
                        db.insert_table("goodbye", "guild_id", "channel_id"),
                        val)
                else:
                    cursor.execute(
                        db.update_table(
                            "goodbye",
                            "channel_id",
                            channel.id,
                            "guild_id",
                            ctx.message.guild.id,
                        ))
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(
                    f"Set the goodbye in guild {ctx.message.guild} to {channel.mention} ,the id of it being {channel.id} and id of guild being {ctx.message.guild.id}"
                )
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**"
                )
        except:
            await ctx.send("Failed to set channel")

    @goodbye.command()
    async def clear(self, ctx: Context):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("goodbye", "channel_id", "guild_id",
                                    ctx.message.guild.id))
                result = cursor.fetchone()
                if result is None:
                    await ctx.send(
                        " Do not have a table for the goodbye channel - Check Database."
                    )
                else:
                    cursor.execute(
                        db.delete_table("goodbye", "guild_id",
                                        ctx.message.guild.id))
                    await ctx.send(" Cleared the table")
                connect.commit()
                cursor.close()
                connect.close()
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("Failed to remove goodbye channel setting")

    @goodbye.command(pass_context=True)
    async def text(self, ctx: Context, *, content=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                if content is None:
                    await ctx.send("Setting default message")
                    content = "A person left, who knows his/hers reasons for leaving but we will welcome them with open arms if they return "

                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("goodbye", "text", "guild_id",
                                    ctx.message.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, content)
                    cursor.execute(
                        db.insert_table("goodbye", "guild_id", "text"), val)
                else:
                    val = (content, ctx.message.guild.id)
                    cursor.execute(
                        "UPDATE goodbye SET text = ? WHERE guild_id = ?", val)
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(" Set the goodbye message text")
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send(" Error , argument may be invalid")


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Other(bot))
    Logger.cog_loaded(bot.get_cog("Other").name)
