import discord
import asyncio
from discord.ext import commands
from scripts import help, db
import sqlite3

class helper(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(invoke_without_command=True) # Команда Help
    async def help(self, ctx):
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(db.select_table("prefixes","prefix","guild_id", ctx.guild.id))
        res = cursor.fetchone()
        cursor.close()
        connect.close()
        if res is None:
            res = "$"
        await ctx.send(help.categories.format(res[0]))
    
    @help.command(pass_context=True)
    async def moderation(self, ctx):
        await ctx.send(help.mod)
    
    @help.command(pass_context=True)
    async def minigames(self, ctx):
        await ctx.send(help.minigames)
    
    @help.command(pass_context=True)
    async def fun(self, ctx):  
        await ctx.send(help.fun)

    @help.command(pass_context=True)
    async def music(self, ctx):
        await ctx.send(help.music)

    @help.command(pass_context=True)
    async def infosystem(self, ctx): 
        await ctx.send(help.infosystem)

    @help.command(pass_context=True)
    async def tools(self, ctx): 
        await ctx.send(help.tools)

    @help.command(pass_context=True)
    async def system(self, ctx):
        await ctx.send(help.system)

    @help.command(pass_context=True)
    async def sudo(self, ctx):
        await ctx.send(help.sudo)
    
    @help.command(pass_context=True)
    async def config(self, ctx):
        await ctx.send(help.config)



    @commands.command()
    async def version(self, ctx):
        path = "scripts/version.txt"
        with open(path, "r") as file:
            ver = file.readline()
        vers = discord.Embed(title="Current version", description=ver, color=0xd12ec9)
        await ctx.send(embed=vers)

    @commands.command()
    async def info(self, ctx):
        path = "scripts/version.txt"
        with open(path, "r") as file:
            ver = file.readline()
        embed = discord.Embed(title="Openbot", description="Opensource moderation and music bot", color=0xff6900)
        embed.add_field(name="Current version", value=ver, inline=False)
        embed.add_field(name="Author", value="Bot based on NigamanRPG#6937 KonsoleBot -English translation + additions by Middlle#7488 ", inline=False)
        embed.add_field(name="Thanks", value="NigamanRPG#6937 for konsolebot code on https://computerteam.tk:4600/ , Plastik#5004 for setname command code ", inline=False)
        embed.add_field(name="Hosting", value="Heroku", inline=False)
        embed.set_footer(text="Openbot", icon_url="https://cdn.discordapp.com/avatars/666304823934844938/c3e9338cdbe1d2ccb1e15288724f8e74.webp?size=1024")
        await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(helper(bot))
