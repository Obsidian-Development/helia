import discord
import asyncio
from datetime import datetime
import functools
import os
from discord.ext import commands
class welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        hellotxt = os.path.join(f"db/welcome/welcome_{member.guild.id}.txt")  
        with open(hellotxt, "r") as file:
            set = file.read()
            setchan = int(set)
        now  = datetime.now()
        time = now.strftime("%H:%M:%S")
        hello = discord.Embed(title="User Entered The Server", description=f"{member.mention} welcome.", color=0x00ff00)
        #hello.add_field(name="Время", value=time, inline=False)
        hello.set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        hello.set_thumbnail(url=f"{member.avatar_url}")
        channel = self.bot.get_channel(setchan)
        await channel.send(embed=hello)

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        await ctx.send("bot: Set A channel for welcome messages")

    @welcome.command(pass_context=True)
    async def channel(self, ctx, chan: discord.TextChannel):
        author =  ctx.message.author
        hellotxt = os.path.join(f"db/welcome/welcome_{author.guild.id}.txt")
        if author.guild_permissions.administrator:
                if os.path.exists(hellotxt):
                    os.remove(hellotxt)
                with open(hellotxt,"a") as welcome_f:
                     welcome_f.write(f"{chan.id}")
                await ctx.send(f"bot: Welcome message channel was set to {chan.mention}")
        
           
    @welcome.command(pass_context=True)
    async def clear(self, ctx):
        author =  ctx.message.author
        if author.guild_permissions.administrator:
            helloclear = os.path.join(f"db/welcome/welcome_{author.guild.id}.txt")
            if os.path.exists(helloclear):
                 os.remove(helloclear)
            await ctx.send("bot: Config File Cleared")
        else:
           await ctx.send("bot: Not Enough Perms. Need permission: **Administrator**")
 
 
 
 


def setup(bot):
    bot.add_cog(welcome(bot))
