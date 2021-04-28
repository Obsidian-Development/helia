import discord
import asyncio
import random
import math
import wikipedia
from scripts import blacklist
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class tools(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(description='Random number generator')
    async def randint(self,ctx: SlashContext, stc1:int, stc2:int):
        result = random.randint(stc1, stc2)
        await ctx.send(f"Randome number geneation between {stc1} and {stc2} equals ``{result}``")
 
    @commands.command(description='Count square root')
    async def sqrt(self, ctx: SlashContext, num:int):
        result = math.sqrt(num)
        await ctx.send(f"Square root of {num} equals ``{result}``")

    @commands.command(description='Generate Embed')
    async def embed(self,ctx: SlashContext, name,*, content):
        creator = discord.Embed(title=name, description=content)
        await ctx.send(embed = creator)
        
    @commands.group(invoke_without_command=True, description='Reminder')
    async def remind(self, ctx: SlashContext):
        rinfo = discord.Embed(title="Reminder Command", description="Used to create a reminder. Time is indicated in seconds.", color=0x00ff00)
        rinfo.add_field(name="Usage", value="``remind role [Role] [Time]`` - reminder for role \n ``remind me [Time] [Message]`` - reminder for you", inline=True)
        await ctx.send(embed=rinfo)

    @remind.command()
    async def me(self,ctx: SlashContext, time:int,*, content):
        author = ctx.message.author
        valid_users = ["663457844460388362"]
        if str(author.id) in valid_users:
            await ctx.send("bot: Not enough rights to use this text in a reminder")
        else:
            await ctx.send(f"bot: Reminder successfully installed, off in {time} seconds")
            await asyncio.sleep(time)
            await ctx.send(f"<:alarm_clock:664007109188255745> **Reminder for {author.mention} :** {content}")

    @remind.command()
    async def role(self,ctx: SlashContext,role:discord.Role, time:int,*, content):
        if blacklist.list in content:
            await ctx.send("bot: Not enough rights to use this text in a reminder")
        else:
            if role.mentionable == True:
                await ctx.send(f"bot: Reminder successfully installed, off in {time} seconds")
                await asyncio.sleep(time)
                await ctx.send(f"<:alarm_clock:664007109188255745> **Reminder for {role.mention} :** {content}")
            else:
                await ctx.send("bot: Not Enough Permissions , Mention another role ")
                
    @commands.command(description='Search Wikipedia')
    async def wiki(self,ctx: SlashContext,*, searcher=None):
        try:
            wikipedia.set_lang("en")
            req = wikipedia.page(searcher)
            wikip = discord.Embed(title=req.title, description="Wikipedia search results", url=req.url, color=0x269926)
            wikip.set_thumbnail(url=req.images[0])
            await ctx.send(embed=wikip)
        except wikipedia.exceptions.PageError:
            await ctx.send("Wikipedia: No page with that name")
        except:
            await ctx.send("bot: Missing argument or permissions to do the command")




def setup(client):
    client.add_cog(tools(client))
