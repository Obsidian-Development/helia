import discord
import asyncio
import os
from discord.ext import commands


class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ticket(self, ctx):
        tinfo = discord.Embed(title="Ticket Command", description="Used for support ticker", color=0x00ff00)
        tinfo.add_field(name="Usage", value="``ticket create`` - create a support ticket", inline=True)
        await ctx.send(embed=tinfo)

    @ticket.command(pass_context=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        author = ctx.message.author
        ticktxt = os.path.join(f"db/tickets/", f"tickets_{author.guild.id}.txt")
        if author.guild_permissions.administrator:
            if os.path.exists(ticktxt):
                os.remove(ticktxt)
            with open(ticktxt, "a") as sub_f:
                sub_f.write(f"{channel.id}")
            await ctx.send(f"bot: Ticket channel set to {channel.mention}")
        else:
            await ctx.send("bot: Not Enough Perms. Need permission: **Administrator**")

    @ticket.command(pass_context=True)
    async def clear(self, ctx):
        author = ctx.message.author
        if author.guild_permissions.administrator:
            tclear = os.path.join(f"db/tickets/"f"tickets_{author.guild.id}.txt")
            if os.path.exists(tclear):
                os.remove(tclear)
            await ctx.send("bot: Config file was cleared")
        else:
            await ctx.send("bot: Not Enough Perms. Need permission: **Administrator**")

    @ticket.command(pass_context=True)
    async def create(self, ctx, *, tekst):
        author = ctx.message.author
        ticktxt = os.path.join(f"db/tickets/", f"tickets_{author.guild.id}.txt")
        with open(ticktxt, "r") as file:
            tset = file.read()
            chan = int(tset)
        channel = self.bot.get_channel(chan)
        tick = discord.Embed(title=f"Ticket by user {author}", color=0x00ff00)
        tick.add_field(name="Description", value=tekst, inline=False)
        tick.set_footer(text=f"OpenBot Ticket System. User ID: {author.id} ")
        await channel.send(embed=tick)

def setup(bot):
    bot.add_cog(tickets(bot))
