import discord
import asyncio
from discord.ext import commands


class mod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['kick'])
    async def userdel(self, ctx, member : discord.Member,*, reason=None ): # pacmanR - кик пользователя
        author = ctx.message.author
        try:
            if author.guild_permissions.kick_members:
                await member.kick(reason=reason)
                await ctx.send(f"bot: User Kicked for: {reason}")
            else:
                embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
                await ctx.send(embed=embed)    

        except discord.errors.Forbidden:
            embed=discord.Embed(title="🔴 Error", description="I need the ``Kick Members`` permission to do this.", color=0xdd2e44,)
            await ctx.send(embed=embed)


    @commands.command(aliases=['ban'])
    async def devnull(self, ctx, member : discord.Member,*, reason=None ): # devnull - бан пользователя
        author = ctx.message.author
        try:
            if author.guild_permissions.ban_members:
                await member.ban(reason=reason)
                await ctx.send(f"bot: User Banned for: {reason}")
            else:
                embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
                await ctx.send(embed=embed)    
        
        except discord.errors.Forbidden:
            embed=discord.Embed(title="🔴 Error", description="I need the ``Ban Members`` permission to do this.", color=0xdd2e44,)
            await ctx.send(embed=embed)    


    @commands.command()
    async def clear(self, ctx,*,number:int=None): # clear - Очистка сообщений
        channel = ctx.guild.get_channel(645307856773578782)
        author = ctx.message.author
        try:
            if author.guild_permissions.manage_messages:
                if number is None:
                   await ctx.send("bot: Enter Quota Of Messages to be purged")
                else:
                   await ctx.channel.purge(limit=number)
                   await ctx.send(f"bot: Cleared Messages")
            else:
                embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
                await ctx.send(embed=embed)       
              
        except discord.errors.Forbidden:
            embed=discord.Embed(title="🔴 Error", description="I need the ``Manage Messages`` permission to do this.", color=0xdd2e44,)
            await ctx.send(embed=embed)     



    @commands.command(aliases=['mute'])
    async def rmmod(self, ctx, member: discord.Member,time,*, reason=None):
        author = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        try:
            author = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if author.guild_permissions.kick_members:
                await member.add_roles(role)
                await ctx.send(f"bot: User muted for: {reason}")
            else:
                embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
                await ctx.send(embed=embed)    

        except discord.errors.Forbidden:
            embed=discord.Embed(title="🔴 Error", description="I need the ``Manage Roles`` permission to do this.", color=0xdd2e44,)
            await ctx.send(embed=embed)        

    @commands.command(aliases=['unmute'])
    async def unrmmod(self, ctx, member: discord.Member):
        author = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        try:
            if author.guild_permissions.kick_members:
                await member.remove_roles(role)
                await ctx.send(f"bot: Unmuted user")
            else:
                embed=discord.Embed(title="You failed", description="You do not have enough permissions", color=0xff0000)
                await ctx.send(embed=embed)    

        except discord.errors.Forbidden:
            embed=discord.Embed(title="🔴 Error", description="I need the ``Manage Roles`` permission to do this.", color=0xdd2e44,)
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
