import discord
import asyncio
import functools
import os
import sqlite3
from scripts import db, help
from discord.ext import commands
class welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(db.select_table("welcome", member.guild.id)) 
        chan = cursor.fetchone()
        if chan is None:
            print(f"Server {member.guild.id} doesent have a set welcome channel")
            return
        else:
             hello = discord.Embed(title="Welcome", description=f"{member} hello there", color=0x00ff00)
             hello.set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
             hello.set_thumbnail(url=f"{member.avatar_url}")
             channel = self.bot.get_channel(id=int(chan[0]))
             await channel.send(embed=hello)      
        cursor.close()
        connect.close()

       


        
    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        await ctx.send(help.welcome)

    @welcome.command(pass_context=True)
    async def channel(self, ctx, chan: discord.TextChannel):
        author = ctx.message.author     
        if author.guild_permissions.administrator:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()   
            cursor.execute(db.select_table("welcome", ctx.guild.id)) 
            res = cursor.fetchone()
            if res is None:
                val = (ctx.guild.id, chan.id)
                cursor.execute(db.insert_table("welcome"), val)
            else:
                cursor.execute(db.update_table("welcome", chan.id, ctx.guild.id))  
            connect.commit()
            cursor.close()
            connect.close()
            await ctx.send(f"bot: Succesfully set the welcome channel to {chan.mention}")  
        else:
            await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")      


    @welcome.command(pass_context=True)
    async def clear(self, ctx):
        author =  ctx.message.author
        if author.guild_permissions.administrator:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("welcome", ctx.guild.id))
            res = cursor.fetchone()
            if res is None:
                await ctx.send("bot: Do not have a table for the welcome channel - Check Database")
            else:
                cursor.execute(db.delete_table("welcome", ctx.guild.id))
                await ctx.send("bot: Cleared Table")
            connect.commit()
            cursor.close()
            connect.close()
        else:
            await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")
       
def setup(bot):
    bot.add_cog(welcome(bot))
