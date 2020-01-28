import discord
from discord.ext import commands

commands_string = """
**Moderation and Administartion Contact Commands Info**
`clear`, `devnull`, `rmmod`, `unrmmod`, `userdel`, `sub`, `ticket`, `shutdown`, `welcome` , `goodbye` , `set_status`


**Other Commands**
`avatar` `guild` `neofetch` `voicedemo` `casino` `kubik` `monetka` `ubuntu ` `mint` `manjaro` `debian` `arch` `echo` `ping`

"""

class GeneralListener(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="OpenBot. Help System",
            colour=discord.Colour(value=11735575).orange()
            )
        embed.add_field(
            name=":tools: **Based On NigamanRPG#6937 KonsoleBot**",
            value="Translated Into English By Middlle#7488"
            )
        embed.add_field(
            name=":books: **Commands** | Prefix: **$**",
            value=commands_string,
            inline=False
            )
        nano_bot = self.client.get_user(self.client.user.id)
        embed.set_thumbnail(url=nano_bot.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def secret(self, ctx):
        await ctx.send(ctx.secret)

    @commands.command()
    async def ping(self, ctx):
        latency = "%.0fms" % (self.client.latency * 100)
        embed = discord.Embed(
            title="{}-bot's Latency'".format(self.client.name),
            type='rich',
            description=":hourglass_flowing_sand:" + latency,
            colour=discord.Colour(value=11735575).orange()
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx, *args):
        await ctx.send(" ".join(args))

    @commands.command()
    async def set_status(self, ctx, *args):
        await self.client.change_presence( activity=discord.Game(" ".join(args)) )


def setup(client):
    client.add_cog(GeneralListener(client))
    print('GeneralListener is Loaded')
