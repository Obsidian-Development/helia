import discord
import asyncio
import sqlite3
from discord.ext import commands

class logs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        delete = discord.Embed(title="Message deleted ", description="Logs")
        delete.add_field(name="Channel", value=f"{message.channel}", inline=False)   
        delete.add_field(name="Contents of the message", value=f"{message.content[1:1024]}", inline=False) 
        delete.add_field(name="Author", value=f"{message.author} (ID: {message.author.id})", inline=False)
        chan = self.bot.get_channel(672681436649881600)
        await chan.send(embed=delete)
        
    @commands.group(invoke_without_command=True)
    async def logs(self, ctx):
        await ctx.send("logs")
    






def setup(bot):
    bot.add_cog(logs(bot)) 