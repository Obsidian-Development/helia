# LOCALIZATION SUPPORT NEEDS IMPLEMENTING

import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext


class gnulinux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # GNU/Linux Distr Wiki
    @commands.command(description="Arch Linux Description")
    async def arch(self, ctx: SlashContext):
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        archl = discord.Embed(
            title="Arch Linux",
            url="https://www.archlinux.org/download/",
            description="Arch Linux is an independent general purpose GNU / Linux distribution optimized for the x86-64 architecture, which aims to provide the latest stable versions of software following the rolling release model. By default, the user is provided with a minimalistic basic system in which the user can add what he needs. Pacman package manager is used to install, uninstall and update packages.",
            color=0x1793D1,
        )
        archl.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Archlinux-vert-dark.svg/1280px-Archlinux-vert-dark.svg.png"
        )
        archl.add_field(name="Suggestions",
                        value="Install it yourself without gui",
                        inline=True)
        await ctx.send(embed=archl)

    @commands.command(description="Ubuntu linux description")
    async def ubuntu(self, ctx: SlashContext):  # Ubuntu
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        ubuntu1 = discord.Embed(
            title="Ubuntu",
            url="https://ubuntu.com/",
            description="Ubuntu is an operating system based on Debian GNU / Linux. The main developer and sponsor is Canonical. Currently, the project is actively developed and supported by the free community.",
            color=0xDE4714,
        )
        ubuntu1.add_field(
            name="Assesement",
            value="Good for users trying linux first time",
            inline=True,
        )
        ubuntu1.set_thumbnail(url="https://i.imgur.com/TfVgK1v.png")
        await ctx.send(embed=ubuntu1)

    @commands.command(description="Debian Linux Description")
    async def debian(self, ctx: SlashContext):  # Debian
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        debian1 = discord.Embed(
            title="Debian",
            url="https://www.debian.org/",
            description="Debian is an open source operating system. Currently, Debian GNU / Linux is one of the most popular and important GNU / Linux distributions, which in its primary form has had a significant impact on the development of this type of OS as a whole. There is also a project based on a different kernel: Debian GNU / Hurd. Debian can be used as an operating system for both servers and workstations.",
            color=0xD80150,
        )
        debian1.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Debian-OpenLogo.svg/800px-Debian-OpenLogo.svg.png"
        )
        await ctx.send(embed=debian1)

    @commands.command(description="Deepin linux description")
    async def deepin(self, ctx: SlashContext):  # Deepin
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        deepin1 = discord.Embed(
            title="Deepin",
            url="https://www.deepin.org",
            description="Deepin (stylized as deepin; formerly known as Linux Deepin and Hiweed Linux) is a Linux distribution based on Debian's stable branch. It features DDE, the Deepin Desktop Environment, built on Qt and available for various distributions like Manjaro, Arch or Fedora. As of version 15.10 it also uses dde-kwin, a set of patches for KDE Plasma's window manager. In 2019, Huawei started to ship Linux laptops pre-installed with deepin. ",
            color=0x1793D1,
        )
        deepin1.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Deepin_logo.svg/600px-Deepin_logo.svg.png"
        )
        await ctx.send(embed=deepin1)

    @commands.command(description="Manjaro linux description")
    async def manjaro(self, ctx: SlashContext):  # Manjaro
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        manjaro1 = discord.Embed(
            title="Manjaro",
            url="https://manjaro.org/",
            description="Manjaro Linux or Manjaro is an Arch Linux GNU / Linux distribution that uses the rolling release update model. Several versions are officially available: with the XFCE, KDE, or GNOME desktop.",
            color=0x35BF5C,
        )
        manjaro1.set_thumbnail(
            url="https://fost.ws/uploads/posts/2019-05/1557568788_manjaro-logo.png"
        )
        manjaro1.add_field(name="Suggestions",
                           value="Good for not complete noobs",
                           inline=True)
        await ctx.send(embed=manjaro1)

    @commands.command(description="Linux Mint description")
    async def mint(self, ctx: SlashContext):  # Mint
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        mint1 = discord.Embed(
            title="Linux Mint",
            url="https://linuxmint.com/",
            description="Linux Mint is a community-developed free Linux distribution based on Ubuntu and Debian that aims to provide the user with a “modern, elegant and user-friendly operating system that is both powerful and easy to use.” Linux Mint provides full support for a variety of multimedia formats, includes some proprietary programs, and comes with an extensive set of open source applications. The founder of the project is Clement Lefebvre, the development team (Mint Linux Team) and the user community are also actively involved in the development. ",
            color=0xB1EA77,
        )
        mint1.set_thumbnail(url="https://i.imgur.com/cyRjcbp.png")
        mint1.add_field(name="Commentary",
                        value="For housewives and noobs",
                        inline=True)
        await ctx.send(embed=mint1)


def setup(bot):
    bot.add_cog(gnulinux(bot))
