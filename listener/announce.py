import discord
import asyncio
import os
from discord.ext import commands

class broadcast(commands.Cog):
  def __init__(self,bot):
      self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def announce(self, ctx, *, content):
    announcement = discord.Embed(color=0x3B88C3)
    author_name = f'{ctx.message.author}'
    announcement.set_author(name=author_name, url=ctx.message.author.avatar_url)
    announcement.add_field(name=f'🌐 A Global  Announcement', value=content)
    announcement.set_footer(text=f'Announced from {ctx.message.guild.name}', icon_url=ctx.message.guild.icon_url)
    sent_counter = 0
    for guild in self.bot.guilds:
        try:
            await guild.text_channels[0].send(embed=announcement)
            sent_counter += 1
        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass
    response = discord.Embed(color=0x77B255, title=f'✅ Announcement sent to {sent_counter} guilds.')
    await ctx.send(embed=response)  
    

    
def setup(bot):
    bot.add_cog(broadcast(bot))     
