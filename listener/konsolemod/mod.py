import discord
import asyncio
from discord.ext import commands


class mod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def userdel(self, ctx, member : discord.Member,*, reason=None ): # pacmanR - кик пользователя
        author = ctx.message.author
        if author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await ctx.send(f"bot: User Removed for: {reason}")
        else:
                await ctx.send("bot: Not Enough Permissions")

    @commands.command()
    async def devnull(self, ctx, member : discord.Member,*, reason=None ): # devnull - бан пользователя
        author = ctx.message.author
        if author.guild_permissions.ban_members:
                await member.ban(reason=reason)
                await ctx.send(f"bot: User Banned for: {reason}")
        else:
                await ctx.send("bot: Not Enough Permissions")

    @commands.command()
    async def clear(self, ctx,*,number:int=None): # clear - Очистка сообщений
        channel = ctx.guild.get_channel(645307856773578782)
        author = ctx.message.author
        if author.guild_permissions.manage_messages:
            if number is None:
                await ctx.send("bot: Enter Quota Of Messages to be purged")
            else:
                await ctx.channel.purge(limit=number)
                await ctx.send(f"bot: Cleared Messages")
        else:
            await ctx.send("bot: Not Enough Permissions")


    @commands.command()
    async def rmmod(self, ctx, member: discord.Member,time,*, reason=None):
        author = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if author.guild_permissions.kick_members:
            await member.add_roles(role)
            await ctx.send(f"bot: User Banned for: {reason}")
            channel = ctx.guild.get_channel(645307856773578782)
            mutemb = discord.Embed(title="User Was Silenced", color=0x00ff00)
            mutemb.add_field(name="User who was silenced", value=member.mention, inline=False)
            mutemb.add_field(name="Silence Time", value=time, inline=False)
            mutemb.add_field(name="Reason", value=reason, inline=False)
            mutemb.add_field(name="Administrator/Moderator", value=f"{ctx.message.author.mention}", inline=False)
            await channel.send(embed=mutemb)

        else:
            await ctx.send("bot: Not Enough Permissions")

    @commands.command()
    async def unrmmod(self, ctx, member: discord.Member):
        author = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if author.guild_permissions.kick_members:
            await member.remove_roles(role)
            await ctx.send(f"bot: User Was Unsilenced")
            channel = ctx.guild.get_channel(645307856773578782)
            unmutemb = discord.Embed(title="User Was Unsilenced", color=0x00ff00)
            unmutemb.add_field(name="User", value=member.mention, inline=False)
            unmutemb.add_field(name="Administrator/Moderator", value=f"{ctx.message.author.mention}", inline=False)
            await channel.send(embed=unmutemb)
        else:
            await ctx.send("bot: Not Enough Permissions")

    @commands.command()
    async def shutdown(ctx): # Команда для выключения бота
        author = ctx.message.author
        if author.id == 540142383270985738:
        await ctx.send("Shutting Down The Bot")
        await ctx.bot.logout()
    else:
        await ctx.send("bot: You dont have enough Permissions for this command : Need perms Bot Owner")      


def setup(bot):
    bot.add_cog(mod(bot))
