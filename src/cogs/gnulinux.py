# LOCALIZATION SUPPORT NEEDS IMPLEMENTING
import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from cogs.utils import Config, Logger, Settings, Strings

CONFIG = Config()



class gnulinux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # GNU/Linux Distr Wiki
    @commands.command(description="Arch Linux Description")
    async def arch(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        archl = discord.Embed(
            title="Arch Linux",
            url="https://www.archlinux.org/download/",
            description=STRINGS["gnulinuxx"]["archdesc"],
            color=0x1793D1,
        )
        archl.set_thumbnail(
            url=
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Archlinux-vert-dark.svg/1280px-Archlinux-vert-dark.svg.png"
        )
        await ctx.send(embed=archl)

    @commands.command(description="Ubuntu linux description")
    async def ubuntu(self, ctx: SlashContext):  # Ubuntu
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        ubuntu1 = discord.Embed(
            title="Ubuntu",
            url="https://ubuntu.com/",
            description=STRINGS["gnulinuxx"]["ubuntudesc"],
            color=0xDE4714,
        )
        ubuntu1.set_thumbnail(url="https://i.imgur.com/TfVgK1v.png")
        await ctx.send(embed=ubuntu1)

    @commands.command(description="Debian Linux Description")
    async def debian(self, ctx: SlashContext):  # Debian
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        debian1 = discord.Embed(
            title="Debian",
            url="https://www.debian.org/",
            description=STRINGS["gnulinuxx"]["debiandesc"],
            color=0xD80150,
        )
        debian1.set_thumbnail(
            url=
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Debian-OpenLogo.svg/800px-Debian-OpenLogo.svg.png"
        )
        await ctx.send(embed=debian1)

    @commands.command(description="Deepin linux description")
    async def deepin(self, ctx: SlashContext):  # Deepin
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        deepin1 = discord.Embed(
            title="Deepin",
            url="https://www.deepin.org",
            description=STRINGS["gnulinuxx"]["deeepindesc"],
            color=0x1793D1,
        )
        deepin1.set_thumbnail(
            url=
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Deepin_logo.svg/600px-Deepin_logo.svg.png"
        )
        await ctx.send(embed=deepin1)

    @commands.command(description="Manjaro linux description")
    async def manjaro(self, ctx: SlashContext):  # Manjaro
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        manjaro1 = discord.Embed(
            title="Manjaro",
            url="https://manjaro.org/",
            description=STRINGS["gnulinuxx"]["manjarodesc"],
            color=0x35BF5C,
        )
        manjaro1.set_thumbnail(
            url=
            "https://fost.ws/uploads/posts/2019-05/1557568788_manjaro-logo.png"
        )
        await ctx.send(embed=manjaro1)

    @commands.command(description="Linux Mint description")
    async def mint(self, ctx: SlashContext):  # Mint
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        mint1 = discord.Embed(
            title="Linux Mint",
            url="https://linuxmint.com/",
            description=STRINGS["gnulinuxx"]["mintdesc"],
            color=0xB1EA77,
        )
        mint1.set_thumbnail(url="https://i.imgur.com/cyRjcbp.png")
        await ctx.send(embed=mint1)


def setup(bot):
    bot.add_cog(gnulinux(bot))
