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
            embed=discord.Embed(title="Action Done", description="User Removed", color=0xff8000)
            await ctx.send(embed=embed)
        else:
                embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
                await ctx.send(embed=embed)

    @commands.command()
    async def devnull(self, ctx, member : discord.Member,*, reason=None ): # devnull - бан пользователя
        author = ctx.message.author
        if author.guild_permissions.ban_members:
                await member.ban(reason=reason)
                embed=discord.Embed(title="Action Done", description="User Banned", color=0xff8000)
                await ctx.send(embed=embed)
        else:
                embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
                await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx,*,number:int=None): # clear - Очистка сообщений
        channel = ctx.guild.get_channel(645307856773578782)
        author = ctx.message.author
        if author.guild_permissions.manage_messages:
            if number is None:
                await ctx.send("bot: Enter Quota Of Messages to be purged")
            else:
                await ctx.channel.purge(limit=number)
                embed=discord.Embed(title="Action Done", description="Cleared Messages", color=0xff8000)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
            await ctx.send(embed=embed)


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
            embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
            await ctx.send(embed=embed)

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
            embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def shutdown(self, ctx): # Команда для выключения бота
        author = ctx.message.author
        valid_users = ["540142383270985738", "573123021598883850"]
        if str(author.id) in valid_users:
            embed=discord.Embed(title="Shutting Down", description="Goodbye", color=0xff8000)
            await ctx.send(embed=embed)
            await ctx.bot.logout()
        else:
            embed2=discord.Embed(title="You failed", description="Need Permission : Bot Owner", color=0xff0000)
            await ctx.send(embed=embed2)         


def setup(bot):
    bot.add_cog(mod(bot))
