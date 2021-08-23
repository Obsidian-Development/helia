# remove .removethisforenable in file name for this cog to load
import asyncio
import functools
import sqlite3
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from scripts import db


class goodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        # now  = datetime.now()
        # time = now.strftime("%H:%M:%S")
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(
            db.select_table("goodbye", "channel_id", "guild_id",
                            member.guild.id))
        chan = cursor.fetchone()
        # print(f" Channel id fetch - {chan[0]}")
        if chan is None:
            return
        cursor.execute(
            db.select_table("goodbye", "text", "guild_id", member.guild.id))
        desc = cursor.fetchone()
        if desc is None:
            desc = f"It seems {member} decided to leave , oh well "
        gb = discord.Embed(
            title="User Left The Channel",
            description=(desc[0]),
            color=0xF4211A,
        )
        # gb.add_field(name="Время", value=time, inline=False)
        gb.set_author(name=f"{member.guild}",
                      icon_url=f"{member.guild.icon_url}")
        gb.set_thumbnail(url=f"{member.avatar_url}")
        channel = self.bot.get_channel(id=int(chan[0]))
        cursor.close()
        connect.close()
        await channel.send(embed=gb)

    @commands.group(invoke_without_command=True)
    async def goodbye(self, ctx: Context):
        await ctx.send("No help information temporarily")

    @goodbye.command()
    async def channel(self, ctx: Context, channel: discord.TextChannel = None):
        try:
            author = ctx.message.author
            if author.guild_permissions.administrator:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("goodbye", "channel_id", "guild_id",
                                    ctx.message.guild.id))
                result = cursor.fetchone()
                if result is None:
                    val = (ctx.message.guild.id, channel.id)
                    cursor.execute(
                        db.insert_table("goodbye", "guild_id", "channel_id"),
                        val)
                else:
                    cursor.execute(
                        db.update_table(
                            "goodbye",
                            "channel_id",
                            channel.id,
                            "guild_id",
                            ctx.message.guild.id,
                        ))
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(
                    f"Set the goodbye in guild {ctx.message.guild} to {channel.mention} ,the id of it being {channel.id} and id of guild being {ctx.message.guild.id}"
                )
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Administrator**"
                )
        except:
            await ctx.send("Failed to set channel")

    @goodbye.command()
    async def clear(self, ctx: Context):
        try:
            author = ctx.message.author
            if author.guild_permissions.administrator:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("goodbye", "channel_id", "guild_id",
                                    ctx.message.guild.id))
                result = cursor.fetchone()
                if result is None:
                    await ctx.send(
                        "bot: Do not have a table for the goodbye channel - Check Database."
                    )
                else:
                    cursor.execute(
                        db.delete_table("goodbye", "guild_id",
                                        ctx.message.guild.id))
                    await ctx.send("bot: Cleared the table")
                connect.commit()
                cursor.close()
                connect.close()
            else:
                await ctx.send(
                    "bot: You do not have enough permissions - :You require **Administrator**."
                )
        except:
            await ctx.send("bot: Error")

    @goodbye.command(pass_context=True)
    async def text(self, ctx: Context, *, content=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.administrator:
                if content is None:
                    return await ctx.send(
                        "bot: Please type the text you wish for the goodbye message"
                    )
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("goodbye", "text", "guild_id",
                                    ctx.message.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, content)
                    cursor.execute(
                        db.insert_table("goodbye", "guild_id", "text"), val)
                else:
                    val = (content, ctx.message.guild.id)
                    cursor.execute(
                        "UPDATE goodbye SET text = ? WHERE guild_id = ?", val)
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send("bot: Set the goodbye message text")
            else:
                await ctx.send(
                    "bot: You do not have enough permissions - :You require **Administrator**."
                )
        except:
            await ctx.send("bot: Error , argument may be invalid")


def setup(bot):
    bot.add_cog(goodbye(bot))
