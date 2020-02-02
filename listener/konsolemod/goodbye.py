import discord
import asyncio
from datetime import datetime
import functools
import sqlite3
from scripts import db
from discord.ext import commands
class goodbye(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        #now  = datetime.now()
        #time = now.strftime("%H:%M:%S")
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(db.select_table("goodbye", member.guild.id))
        chan = cursor.fetchone()
        if chan is None:
            print(f"Server {member.guild.id} doesent have a set goodbye channel")
            return
        else:
            gb = discord.Embed(title="User left the channel", description=f"{member} goodbye", color=0xf4211a)
            #gb.add_field(name="Время", value=time, inline=False)
            gb.set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            gb.set_thumbnail(url=f"{member.avatar_url}")
            channel = self.bot.get_channel(id=int(chan[0]))
        cursor.close()
        connect.close()  
        await channel.send(embed=gb)


    @commands.group(invoke_without_command=True)
    async def goodbye(self, ctx):
        await ctx.send("bot: Set a goodbye channel")

    @goodbye.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        author =  ctx.message.author     
        if author.guild_permissions.administrator: 
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("goodbye", ctx.guild.id))
            result = cursor.fetchone()
            if result is None:
                val = (ctx.guild.id, channel.id)
                cursor.execute(db.insert_table("goodbye"), val)
            else:
                cursor.execute(db.update_table("goodbye", channel.id, ctx.guild.id))
            connect.commit()
            cursor.close()
            connect.close()
            await ctx.send(f"bot: Succesufully set the farewell channel to {channel.mention}")
        else:
            await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")

                
    @goodbye.command()
    async def clear(self, ctx):
        author =  ctx.message.author
        if author.guild_permissions.administrator:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("goodbye", ctx.guild.id))
            result = cursor.fetchone()
            if result is None:
                await ctx.send("bot: Do not have a table for the welcome channel - Check Database")
            else:
                cursor.execute(db.delete_table("goodbye", ctx.guild.id))
                await ctx.send("bot: Cleared The Table")  
            connect.commit()
            cursor.close()
            connect.close()  
        else:
           await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")


def setup(bot):
    bot.add_cog(goodbye(bot))