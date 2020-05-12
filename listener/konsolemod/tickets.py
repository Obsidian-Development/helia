import discord
import asyncio
import sqlite3
from scripts import db, help
from discord.ext import commands


class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ticket(self, ctx):
        await ctx.send(help.tickets)

    @ticket.command(pass_context=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        author = ctx.message.author
        if author.guild_permissions.administrator:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("ticket", ctx.guild.id))
            result = cursor.fetchone()
            if result is None:
                val = (ctx.guild.id, channel.id)
                cursor.execute(db.insert_table("ticket"), val)
            else:
                cursor.execute(db.update_table("ticket", channel.id, ctx.guild.id))
            connect.commit()
            cursor.close()
            connect.close()        
            await ctx.send(f"bot: Set the ticket channel to  {channel.mention}")
        else:
            await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")

    @ticket.command(pass_context=True)
    async def clear(self, ctx):
        author = ctx.message.author
        if author.guild_permissions.administrator:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("ticket", ctx.guild.id))
            result = cursor.fetchone()
            if result is None:
                await ctx.send("bot: Do not have a table for the ticket channel - Check Database")
            else:
                cursor.execute(db.delete_table("ticket", ctx.guild.id))
                await ctx.send("bot: Cleared the table")  
            connect.commit()
            cursor.close()
            connect.close()                
        else:
            await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")

    @ticket.command(pass_context=True)
    async def create(self, ctx, *, tekst):
        author = ctx.message.author
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(db.select_table("ticket", ctx.guild.id)) 
        chan = cursor.fetchone()
        if chan is None:
            await ctx.send("bot: Do not have a activated ticket channel")
            return
        channel = self.bot.get_channel(id=int(chan[0]))
        tick = discord.Embed(title=f"Ticket coming from {author}", color=0x00ff00)
        tick.add_field(name="Description", value=tekst, inline=False)
        tick.set_footer(text=f"Ticket System Openbot. User ID: {author.id} ")
        await channel.send(embed=tick)
        connect.commit()
        cursor.close()
        connect.close()

def setup(bot):
    bot.add_cog(tickets(bot))
