import discord
import asyncio
from discord.ext import commands
from scripts import help

class helper(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

   
    
    @commands.group(invoke_without_command=True) # Команда Help
    async def help(self, ctx): 
        await ctx.send(help.categories)
    
    @help.command(pass_context=True)
    async def moderation(self, ctx): #сдел
        await ctx.send(help.mod)
    
    @help.command(pass_context=True)
    async def minigames(self, ctx): #нн
        await ctx.send(help.minigames)
    
    @help.command(pass_context=True)
    async def fun(self, ctx):  # СДЕЛ
        await ctx.send(help.fun)

    @help.command(pass_context=True)
    async def infosystem(self, ctx): #сдел
        await ctx.send(help.infosystem)

    @help.command(pass_context=True)
    async def tools(self, ctx): #сдел
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
        embed = discord.Embed(title="OpenBot", description="Bot imitating bash and linux terminal", color=0xff6900)
        embed.add_field(name="Current version", value=ver, inline=False)
        embed.add_field(name="Author", value="Bot based on NigamanRPG#6937 KonsoleBot -English translation + additions by Middlle#7488 ", inline=False)
        embed.add_field(name="Thanks", value="NigamanRPG#6937 for konsolebot code on https://computerteam.tk:4600/ , Plastik#5004 for setname command code ", inline=False)
        embed.add_field(name="Hosting", value="Okteto", inline=False)
        embed.set_footer(text="Openbot", icon_url="https://cdn.discordapp.com/avatars/666304823934844938/4a2b2b8de59275e0986de9de582acb25.webp?size=1024")
        await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(helper(bot))
