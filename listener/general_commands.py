import discord
from discord.ext import commands

commands_string = """
**Moderation and Administartion Contact Commands Info**
`clear`, `devnull`(alias `ban`), `rmmod`, `unrmmod`, `userdel`(alias `kick`), `sub`, `ticket`, `shutdown`, `welcome` , `goodbye` , `set_status`

**Utility Commands**
`embed` `randint` `remind` `sqrt` `wallpaper`

**Other Commands**
`avatar` `guild` `neofetch` `voicedemo` `casino` `kubik` `monetka` `ubuntu ` `mint` `manjaro` `debian` `arch` `echo` `ping` `deepin` `setname`

**SOURCE CODE**
"https://github.com/pieckenst/openbot"

**Hosting**
"Heroku (due to dependency on sqlite , bye bye saving set welcome and goodbye channels)"

**Use $invite for getting bot invite links**

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
    async def ping(self, ctx):
        latency = "%.0fms" % (self.client.latency * 100)
        embed = discord.Embed(
            title="{}-Latency'".format(self.client.name),
            type='rich',
            description=":hourglass_flowing_sand:" + latency,
            colour=discord.Colour(value=11735575).orange()
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx, *args):
        await ctx.send(" ".join(args))

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Recomended Functionality Bot Invite", colour=discord.Colour(0xff6900), url="https://discordapp.com/oauth2/authorize?client_id=666304823934844938&scope=bot&permissions=2146958545", description="Bot invite Links")
        embed.set_author(name="Basic Functionality Bot Invite", url="https://discordapp.com/oauth2/authorize?client_id=666304823934844938&scope=bot&permissions=67213505")
        embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/666304823934844938/4a2b2b8de59275e0986de9de582acb25.webp?size=1024")
        await ctx.send(embed=embed)

    @commands.command()
    async def set_status(self, ctx, *args):
        author = ctx.message.author
        valid_users = ["540142383270985738", "573123021598883850"]
        if str(author.id) in valid_users:
            await self.client.change_presence( activity=discord.Game(" ".join(args)) )
            embed=discord.Embed(title="Рапорт", description="Ваш приказ выполнен о владыка ", color=0xff8000)
            embed.add_field(name="English", value="Your orders were done My Lord", inline=True)
            embed.set_footer(text="Openbot")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="You failed", description="Need Permission : Bot Owner", color=0xff0000)
            await ctx.send(embed=embed)      



def setup(client):
    client.add_cog(GeneralListener(client))
    print('GeneralListener is Loaded')
