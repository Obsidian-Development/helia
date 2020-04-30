import discord
import asyncio
from discord.ext import commands


class mod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['kick'])
    async def userdel(self, ctx, member : discord.Member,*, reason=None ): # pacmanR - кик пользователя
        try:
            author = ctx.message.author
            if author.guild_permissions.kick_members:
                if member is None:
                    return await ctx.send("bot: Mention the user you wish to kick") 
                if member is author:
                    return await ctx.send("bot: Hey you cannot kick yourself ")
                if member.guild_permissions.administrator:
                    return await ctx.send("bot: Hey you cannot fucking kick an administrator ") 
                await member.kick(reason=reason)
                await ctx.send(f"bot: User Kicked for: {reason}")
            else:
                embed=discord.Embed(title="🔴 Error", description="You need the permission: **Kick Members** to do this.", color=0xff0000)
                await ctx.send(embed=embed) 
        except discord.errors.Forbidden:
            embed=discord.Embed(title="🔴 Error", description="I need the ``Kick Members`` permission to do this.", color=0xdd2e44,)
            await ctx.send(embed=embed)


    @commands.command(aliases=['ban'])
    async def devnull(self, ctx, member : discord.Member,*, reason=None ): # devnull - бан пользователя
        try:
            author = ctx.message.author
            if author.guild_permissions.ban_members:          
                if member is None:
                    return await ctx.send("bot: Mention the user you wish to ban")
                if member is author:
                    return await ctx.send("bot: Hey you cannot ban yourself")
                if member.guild_permissions.administrator:
                    return await ctx.send("bot: Hey you cannot fucking ban an administrator")
                await member.ban(reason=reason)
                await ctx.send(f"bot: User Banned for : {reason}")
            else:
                embed=discord.Embed(title="🔴 Error", description="You need the permission: **Ban Members** to do this.", color=0xff0000)
                await ctx.send(embed=embed) 
        except:
            embed=discord.Embed(title="🔴 Error", description="I need the ``Ban Members`` permission to do this.", color=0xdd2e44,)
            await ctx.send(embed=embed)   


    @commands.group(invoke_without_command=True)
    async def clear(self, ctx,*,number:int=None): # clear - Очистка сообщений
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_messages:
                if number <= 0:
                    return await ctx.send("bot: Enter a number of messages to be purged starting from 1")
                else:
                    number = number + 1
                    await ctx.channel.purge(limit=number)
                    msg = await ctx.send(f"bot: Cleared the amount of messages")
                    await asyncio.sleep(2)
                    await discord.Message.delete(msg)
            else:
               embed=discord.Embed(title="🔴 Error", description="You need the permission: **Manage Messages** to do this.", color=0xff0000)
               await ctx.send(embed=embed)
        except discord.errors.Forbidden:
            embed=discord.Embed(title="🔴 Error", description="I need the ``Manage Messages`` permission to do this.", color=0xdd2e44,)
            await ctx.send(embed=embed)
            
    @clear.command(pass_context=True) 
    async def user(self,ctx,member=None,*, amount:int=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_messages:           
                if member is None or amount is None:                                
                    return await ctx.send("bot: Mention the user and the number of messages you wish to purge")                                                                                
                user = await commands.MemberConverter().convert(ctx, member)  
                await ctx.message.delete()                                                                     
                await ctx.channel.purge(limit=amount, check=lambda m: m.author == user)                                                                                                                                                                                                       
                successmessage = await ctx.send(f"bot: Cleared the messages from {user.mention}")    
                await asyncio.sleep(2)          
                await successmessage.delete() 
            else:
               embed=discord.Embed(title="🔴 Error", description="You need the permission: **Manage Messages** to do this.", color=0xff0000)
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
            await ctx.bot.change_presence(activity=discord.Game(name="Вырубаемся нахуй"))
            await asyncio.sleep(5)
            await ctx.bot.logout()
        else:
            embed2=discord.Embed(title="🔴 Error", description="You need the ``Bot Owner`` permission to do this.", color=0xdd2e44,)
            await ctx.send(embed=embed2) 
    



def setup(bot):
    bot.add_cog(mod(bot))
