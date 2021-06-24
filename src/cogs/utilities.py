# -*- coding: utf-8 -*-
import math
import random
import re
from typing import NoReturn

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord_slash import SlashContext, cog_ext

from cogs.utils import Config, Logger, Settings, Strings

CONFIG = Config()


class Utilities(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Utilities"

    @commands.command()
    @commands.guild_only()
    async def user(self,
                   ctx: Context,
                   member: discord.Member = None) -> NoReturn:
        """Shows user information.

        Attributes:
        -----------
        - `member` - user

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if member is None:
            member = ctx.message.author

        id = str(member.id)
        name = member.name
        tag = member.discriminator
        username = member.nick
        joined_at = member.joined_at.strftime("%d.%m.%Y %H:%M")
        created_at = member.created_at.strftime("%d.%m.%Y %H:%M")
        stat = member.status
        activ = member.activity
        color = member.color
        avatar = member.avatar_url_as()

        embed = discord.Embed(
            description=STRINGS["utilities"]["user_info"].format(
                id, created_at, joined_at, username, stat, activ, color),
            color=color,
        )
        embed.set_author(
            name=STRINGS["utilities"]["user_info_title"].format(name, tag))
        embed.set_thumbnail(url=avatar)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def emoji(self, ctx: Context, emoji: str) -> NoReturn:
        """Shows emoji information."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        format = r"png" if re.sub(r"[\<]", r"",
                                  emoji.split(":")[0]) == "" else "gif"
        name = emoji.split(":")[1]
        id = re.sub(r"[\>]", r"", emoji.split(r":")[2])

        embed = discord.Embed(
            title=STRINGS["utilities"]["emoji_info_title"].format(name),
            color=0xEDA84E)
        embed.set_image(url=f"https://cdn.discordapp.com/emojis/{id}.{format}")
        embed.set_footer(text=STRINGS["utilities"]["emoji_info"].format(id))

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def channel(self, ctx: Context, channel: str) -> NoReturn:
        """Shows channel information."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if re.search(r"[@&\:]", channel) is None:

            channel = discord.utils.get(ctx.guild.channels,
                                        id=int(re.sub("[<#>]", "", channel)))

            if (channel.type
                    == discord.ChannelType.text) or channel.type not in [
                        discord.ChannelType.voice,
                        discord.ChannelType.news,
            ]:
                type = STRINGS["etc"]["channel_type"]["text"]
            elif channel.type == discord.ChannelType.voice:
                type = STRINGS["etc"]["channel_type"]["voice"]
            else:
                type = STRINGS["etc"]["channel_type"]["news"]
            if channel.nsfw:
                is_nsfw = STRINGS["etc"]["other"]["yes"]
            else:
                is_nsfw = STRINGS["etc"]["other"]["no"]

            name = channel.name
            id = channel.id
            created_at = channel.created_at.strftime("%d.%m.%Y %H:%M")

            embed = discord.Embed(
                description=STRINGS["utilities"]["channel_info"].format(
                    id, type, created_at, is_nsfw),
                color=0xEDA84E,
            )
            embed.set_author(
                name=STRINGS["utilities"]["channel_info_title"].format(name))
            await ctx.send(embed=embed)

        else:
            await ctx.send("чел, это не канал, ты что-то попутал")

    @commands.command()
    @commands.guild_only()
    async def avatar(self,
                     ctx: Context,
                     member: discord.Member = None) -> NoReturn:
        """Shows user's avatar.

        Attributes:
        -----------
        - `member` - user

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if member is None:
            member = ctx.message.author
        name = member.name
        tag = member.discriminator
        avatar = member.avatar_url_as()
        hash = member.avatar

        embed = discord.Embed(
            color=0xEDA84E,
            title=STRINGS["utilities"]["avatar_info_title"].format(name, tag),
            description=STRINGS["utilities"]["avatar_info"].format(
                hash, avatar),
        )
        embed.set_image(url=avatar)

        await ctx.send(embed=embed)

    @commands.command(description="Random number generator")
    async def randint(self, ctx: SlashContext, stc1: int, stc2: int):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        result = random.randint(stc1, stc2)
        embed = discord.Embed(
            title=STRINGS["generictext"]["randinttitle"],
            description=STRINGS["generictext"]["descgenermath"],
        )
        embed.add_field(name=STRINGS["generictext"]["numberone"],
                        value=f"```{stc1}```",
                        inline=True)
        embed.add_field(name=STRINGS["generictext"]["numbertwo"],
                        value=f"```{stc2}```",
                        inline=True)
        embed.add_field(name=STRINGS["generictext"]["result"],
                        value=f"```{result}```",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(description="Count square root")
    async def sqrt(self, ctx: SlashContext, num: int):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        if num > 5000 or num < 0:
            embed = discord.Embed(
                title=STRINGS["error"]["on_error_title"],
                description=STRINGS["error"]["localeerrortext"],
                color=0xFF0000,
            )
            embed.add_field(
                name=STRINGS["generictext"]["invalidvalue"],
                value=STRINGS["generictext"]["valmath"],
                inline=False,
            )
            await ctx.send(embed=embed)
            return
        else:
            result = math.sqrt(num)
            embed = discord.Embed(
                title=STRINGS["generictext"]["sqsqrt"],
                description=STRINGS["generictext"]["math"],
            )
            embed.add_field(
                name=STRINGS["generictext"]["entered"],
                value=f"```{num}```",
                inline=False,
            )
            embed.add_field(
                name=STRINGS["generictext"]["result"],
                value=f"```{result}```",
                inline=True,
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["server"])
    @commands.guild_only()
    async def guild(self, ctx: Context) -> NoReturn:
        """Shows guild information."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        guild = ctx.guild
        id = ctx.guild.id
        banner = guild.banner_url_as()
        icon = guild.icon_url_as()
        created_at = guild.created_at.strftime("%d.%m.%Y %H:%M")
        members = len(guild.members)
        owner = guild.owner

        if guild.verification_level == discord.VerificationLevel.none:
            vf = STRINGS["etc"]["levels"]["none"]
        elif guild.verification_level == discord.VerificationLevel.low:
            vf = STRINGS["etc"]["levels"]["low"]
        elif guild.verification_level == discord.VerificationLevel.medium:
            vf = STRINGS["etc"]["levels"]["medium"]
        elif guild.verification_level == discord.VerificationLevel.high:
            vf = STRINGS["etc"]["levels"]["high"]
        elif guild.verification_level == discord.VerificationLevel.extreme:
            vf = STRINGS["etc"]["levels"]["extreme"]
        else:
            vf = STRINGS["etc"]["levels"]["unknown"]

        if guild.explicit_content_filter == discord.ContentFilter.disabled:
            cf = STRINGS["etc"]["levels"]["none"]
        elif guild.explicit_content_filter == discord.ContentFilter.no_role:
            cf = STRINGS["etc"]["levels"]["medium"]
        elif guild.explicit_content_filter == discord.ContentFilter.all_members:
            cf = STRINGS["etc"]["levels"]["high"]
        else:
            cf = STRINGS["etc"]["levels"]["unknown"]

        embed = discord.Embed(
            description=STRINGS["utilities"]["guild_info"].format(
                id, created_at, members, f"<@!{owner.id}>", vf, cf),
            color=0xEDA84E,
        )
        embed.set_author(
            name=STRINGS["utilities"]["guild_info_title"].format(guild))
        embed.set_thumbnail(url=icon)
        embed.set_image(url=banner)

        await ctx.send(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Utilities(bot))
    Logger.cog_loaded(bot.get_cog("Utilities").name)
