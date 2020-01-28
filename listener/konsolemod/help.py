
import discord
import asyncio
import os
from discord.ext import commands

commands_string = """
**Moderation and Administartion Contact Commands Info**
`clear`, `devnull`, `rmmod`, `unrmmod`, `userdel`, `sub`, `ticket`, `shutdown`, `welcome` , `goodbye`

**Utility Commands**
`embed` `factorial` `randint` `remind` `sqrt` `wallpaper`

**Other Commands**
`avatar` `guild` `neofetch` `voicedemo` `casino` `kubik` `monetka` `ubuntu ` `mint` `manjaro` `debian` `arch` `echo` `ping`

"""

class help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="OpenBot. Commands",
            colour=discord.Colour(value=11735575).orange()
            )
        embed.add_field(
            name=":tools: **Based On KonsoleBot By NigamanRPG#6937**",
            value="English Translation - Middlle#7488"
            )
        embed.add_field(
            name=":books: **Commands** | Prefix: **$**",
            value=commands_string,
            inline=False
            )
        nano_bot = self.client.get_user(self.client.user.id)
        embed.set_thumbnail(url=nano_bot.avatar_url)
        await ctx.send(embed=embed)

    




def setup(bot):
    bot.add_cog(help(bot))