import discord
import asyncio
import sqlite3
from scripts import db, help
from discord.ext import commands


class submits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def sub(self, ctx):
        await ctx.send(help.submit)

    @sub.command(pass_context=True)
    async def create(self, ctx, *, arg):
        author = ctx.message.author    
        if author.guild_permissions.manage_messages:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("submit", ctx.guild.id)) 
            chan = cursor.fetchone()
            if chan is None:
                await ctx.send("bot: Do not have a set suggestion channel")
                return
            else:
                channel = self.bot.get_channel(id=int(chan[0]))
                user = ctx.message.author
                submit = discord.Embed(title=f"<:speech_balloon:644199603033473055> Suggestion from {user}", description=arg, color=0x00ff00)
                msg = await channel.send(embed=submit)
                emoj = self.bot.get_emoji(656155011687907358)
                emoj2 = self.bot.get_emoji(656155011746889758)
                await msg.add_reaction(emoj)
                await msg.add_reaction(emoj2)
            connect.commit()
            cursor.close()
            connect.close()     
        else:
            await ctx.send("bot: You do not have enough permissions: You Require  **Manage Messages**")

                     

    @sub.command(pass_context=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        author = ctx.message.author
        if author.guild_permissions.administrator:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("submit", ctx.guild.id))
            result = cursor.fetchone()
            if result is None:
                val = (ctx.guild.id, channel.id)
                cursor.execute(db.insert_table("submit"), val)
            else:
                cursor.execute(db.update_table("submit", channel.id, ctx.guild.id))
            connect.commit()
            cursor.close()
            connect.close()
            await ctx.send(f"bot: Set the suggestion channel to  {channel.mention}")
        else:
            await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")

    @sub.command(pass_context=True)
    async def clear(self, ctx):
        author = ctx.message.author
        if author.guild_permissions.administrator:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("submit", ctx.guild.id))
            result = cursor.fetchone()
            if result is None:
                await ctx.send("bot: Do not have a table for the suggestion channel - Check Database")
            else:
                cursor.execute(db.delete_table("submit", ctx.guild.id))
                await ctx.send("bot: Cleared the table")  
            connect.commit()
            cursor.close()
            connect.close()        
        else:
            await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")


def setup(bot):
    bot.add_cog(submits(bot))
