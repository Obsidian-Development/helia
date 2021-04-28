import discord
import asyncio
import os
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class broadcast(commands.Cog):
  def __init__(self,bot):
      self.bot = bot

  @commands.command(description='Global Announcement from bot owner')
  @commands.is_owner()
  async def announce(self, ctx: SlashContext, *, content):
    announcement = discord.Embed(color=0x3B88C3)
    author_name = f'{ctx.message.author}'
    announcement.set_author(name=author_name, url=ctx.message.author.avatar_url)
    announcement.add_field(name=f'🌐 Global  Announcement', value=content)
    announcement.set_footer(text=f'Announced from {ctx.message.guild.name}', icon_url=ctx.message.guild.icon_url)
    sent_counter = 0
    text_channel_list = []
    embed=discord.Embed(title="Global Announcement System 🌐", description="✅ Announcement sending/sent to guilds.")
    embed.set_author(name=self.bot.user.name)
    await ctx.send(embed=embed)
    for guild in self.bot.guilds:
            try:
                  await guild.text_channels[0].send(embed=announcement)
                  sent_counter += 1
            except discord.Forbidden:
                continue
            except discord.NotFound:
                continue
          
  #@commands.command(description='Debug info')
  #@commands.is_owner()
  #async def debug(self, ctx: SlashContext):
    #voice_states = ctx.bot.voice_clients
    #await ctx.send(f'I am currently in {len(voice_states)} voice channels')
  
    

    
def setup(bot):
    bot.add_cog(broadcast(bot))     
