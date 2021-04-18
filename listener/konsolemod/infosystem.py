import discord
import asyncio
import os
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class infosystem(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(description='User Information')
    async def neofetch(self, ctx: SlashContext , member : discord.Member=None  ):
        if member is None:
            member = ctx.message.author  
        username = member.nick
        join = member.joined_at
        stat = member.status
        activ = member.activity
        ava = member.avatar_url
        id = member.id
        create = member.created_at
        neoembed = discord.Embed(title="User Information", color=0x00ff00)
        neoembed.add_field(name="Tag", value=member, inline=False)
        neoembed.add_field(name="Status", value=stat, inline=False)
        neoembed.add_field(name="Local Username", value=username, inline=False)
        neoembed.add_field(name="User ID", value=id, inline=False)
        neoembed.add_field(name="Date of server entrance", value=join, inline=False)
        neoembed.add_field(name="Account Creation Date", value=create, inline=False)
        neoembed.add_field(name="Activity", value=activ, inline=False)
        neoembed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=neoembed)

    @commands.command(description='User Profile picture')
    async def avatar(self, ctx: SlashContext, member : discord.Member=None):
        if member is None:
            member = ctx.message.author
        avaembed = discord.Embed(title=f"User Profile Picture {member}",color=0x00ff00)
        avaembed.set_image(url=member.avatar_url)
        avaembed.set_footer(text=f"User ID: {member.id}")
        await ctx.send(embed=avaembed)

    @commands.command(description='Server Information')
    async def guild(self, ctx: SlashContext):
        member = ctx.message.author
        servinfo = discord.Embed(title="Server Information", color=0x00ff00)
        servinfo.set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        servinfo.add_field(name="Voice Region", value=f"{member.guild.region}", inline=True)
        servinfo.set_thumbnail(url=f"{member.guild.icon_url}")
        servinfo.add_field(name="Owner", value=f"{member.guild.owner.mention}", inline=True)
        servinfo.add_field(name="Protection Level", value=f"{member.guild.verification_level}", inline=False)
        servinfo.add_field(name="User Count", value=f"{member.guild.member_count}", inline=True)
        servinfo.add_field(name="ID", value=f"{member.guild.id}", inline=False)
        await ctx.send(embed=servinfo)
    
    @commands.command(pass_context=True)
    async def voicedemo(self,ctx: SlashContext, voice: discord.VoiceChannel):
        member = ctx.message.author
        await ctx.send(f"**Voice Channel Screenshare Link {voice.mention}**: https://discordapp.com/channels/{member.guild.id}/{voice.id}")
        



def setup(bot):
    bot.add_cog(infosystem(bot)) 

