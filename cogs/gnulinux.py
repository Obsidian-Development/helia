import discord
import asyncio
from discord.ext import commands

class gnulinux(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command() # GNU/Linux Distr Wiki
    async def arch(self, ctx):
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        archl = discord.Embed(title="Arch Linux", url="https://www.archlinux.org/download/", description="Arch Linux is an independent general purpose GNU / Linux distribution optimized for the x86-64 architecture, which aims to provide the latest stable versions of software following the rolling release model. By default, the user is provided with a minimalistic basic system in which the user can add what he needs. Pacman package manager is used to install, uninstall and update packages.", color=0x1793d1)
        archl.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Archlinux-vert-dark.svg/1280px-Archlinux-vert-dark.svg.png")
        archl.add_field(name="Suggestions", value="Install it yourself without gui", inline=True)
        await ctx.send(embed=archl)

    @commands.command()
    async def ubuntu(self, ctx): # Ubuntu
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        ubuntu1=discord.Embed(title="Ubuntu", url="https://ubuntu.com/", description="Ubuntu is an operating system based on Debian GNU / Linux. The main developer and sponsor is Canonical. Currently, the project is actively developed and supported by the free community.", color=0xde4714)
        ubuntu1.add_field(name="Assesement", value="Good for users trying linux first time", inline=True)
        ubuntu1.set_thumbnail(url="https://i.imgur.com/TfVgK1v.png")
        await ctx.send(embed=ubuntu1)

    @commands.command()
    async def debian(self, ctx): # Debian
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        debian1=discord.Embed(title="Debian", url="https://www.debian.org/", description="Debian is an open source operating system. Currently, Debian GNU / Linux is one of the most popular and important GNU / Linux distributions, which in its primary form has had a significant impact on the development of this type of OS as a whole. There is also a project based on a different kernel: Debian GNU / Hurd. Debian can be used as an operating system for both servers and workstations.", color=0xd80150)
        debian1.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Debian-OpenLogo.svg/800px-Debian-OpenLogo.svg.png")
        await ctx.send(embed=debian1)

    @commands.command()
    async def manjaro(self, ctx): # Manjaro
         channel = ctx.message.channel
         await ctx.send("bot: It Will Be Done - Command Result Below")
         manjaro1=discord.Embed(title="Manjaro", url="https://manjaro.org/", description="Manjaro Linux or Manjaro is an Arch Linux GNU / Linux distribution that uses the rolling release update model. Several versions are officially available: with the XFCE, KDE, or GNOME desktop.", color=0x35bf5c)
         manjaro1.set_thumbnail(url="https://fost.ws/uploads/posts/2019-05/1557568788_manjaro-logo.png")
         manjaro1.add_field(name="Suggestions", value="Good for not complete noobs", inline=True)
         await ctx.send(embed=manjaro1)

    @commands.command()
    async def mint(self, ctx): # Mint
        channel = ctx.message.channel
        await ctx.send("bot: It Will Be Done - Command Result Below")
        mint1=discord.Embed(title="Linux Mint", url="https://linuxmint.com/", description="Linux Mint is a community-developed free Linux distribution based on Ubuntu and Debian that aims to provide the user with a “modern, elegant and user-friendly operating system that is both powerful and easy to use.” Linux Mint provides full support for a variety of multimedia formats, includes some proprietary programs, and comes with an extensive set of open source applications. The founder of the project is Clement Lefebvre, the development team (Mint Linux Team) and the user community are also actively involved in the development. ", color=0xb1ea77)
        mint1.set_thumbnail(url="https://i.imgur.com/cyRjcbp.png")
        mint1.add_field(name="Commentary", value="For housewives and noobs", inline=True)
        await ctx.send(embed=mint1)




def setup(bot):
    bot.add_cog(gnulinux(bot))
