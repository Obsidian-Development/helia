import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from datetime import datetime, timedelta
from scripts.time import pretty_datetime, pretty_timedelta

commands_string = """
**Moderation and Administartion Contact Commands Info**
`clear`, `devnull`, `rmmod`, `unrmmod`, `userdel`, `sub`, `ticket`, `shutdown`, `welcome` , `goodbye` , `set_status`

**Utility Commands**
`embed` `randint` `remind` `sqrt` `wallpaper`

**Other Commands**
`avatar` `guild` `neofetch` `voicedemo` `casino` `kubik` `monetka` `ubuntu ` `mint` `manjaro` `debian` `arch` `echo` `ping` `deepin` `setname`

**Invite The Bot To Your Server**
"https://discordapp.com/oauth2/authorize?client_id=666304823934844938&scope=bot&permissions=8"

**SOURCE CODE**
"https://github.com/pieckenst/Openbot"

"""

class GeneralListener(commands.Cog):

    def __init__(self, client):
        self.client = client



    @commands.command(description='Check Ping')
    async def ping(self, ctx: SlashContext):
        '''Check response time.'''

        msg = await ctx.send('Wait...')

        await msg.edit(content='Response: {}.\nGateway: {}'.format(
	   pretty_timedelta(msg.created_at - ctx.message.created_at),
	   pretty_timedelta(timedelta(seconds=self.client.latency))
	)
	)

    @commands.command(description='Say things as bot')
    async def say(self, ctx: SlashContext, *args):
        await ctx.send(" ".join(args))


    #@commands.command(description='...')
    #async def shh(self, ctx):
        #await ctx.send("Windows 10, china goverment edition, https://rutracker.org/forum/viewtopic.php?t=5752397")

    @commands.command(description='Bot invite links')
    async def invite(self, ctx: SlashContext):
        embed = discord.Embed(title="Recomended Functionality Bot Invite", colour=discord.Colour(0xff6900), url="https://discord.com/api/oauth2/authorize?client_id=666304823934844938&permissions=204859462&scope=applications.commands%20bot", description="Bot invite Links")
        embed.set_author(name="Basic Functionality Bot Invite", url="https://discord.com/oauth2/authorize?client_id=666304823934844938&scope=bot&permissions=204557314")
        embed.add_field(name="Bot up on bots.server-discord.com", value="https://bots.server-discord.com/666304823934844938", inline=True)
        embed.add_field(name="Bot up on top.gg", value="https://top.gg/bot/666304823934844938", inline=True)
        embed.add_field(name="Bot up on bots on discord", value="https://bots.ondiscord.xyz/bots/666304823934844938", inline=True)
        embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description='Set bot status')
    async def set_status(self, ctx, *args):
        author = ctx.message.author
        valid_users = ["540142383270985738", "573123021598883850", "584377789969596416", "106451437839499264", "237984877604110336", "579750505736044574", "497406228364787717"]
        if str(author.id) in valid_users:
            await self.client.change_presence( activity=discord.Game(" ".join(args)) )
            embed=discord.Embed(title="Рапорт", description="Ваш приказ выполнен о владыка ", color=0xff8000)
            embed.add_field(name="English", value="Your orders were done My Lord", inline=True)
            embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="You failed", description="Need Permission : Bot Owner", color=0xff0000)
            await ctx.send(embed=embed)     



def setup(client):
    client.add_cog(GeneralListener(client))
    print('GeneralListener is Loaded')
