import discord
import asyncio
import random
from scripts import games 
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from cogs.utils import Logger, Settings, Config, Strings


CONFIG = Config()

class minigames(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(description='Random cube')
    async def kubik(self, ctx: SlashContext): #кубик рандом
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        kuboid = random.choice(games.kubik)
        embedkub = discord.Embed(title=STRINGS['other']['rollcubetitle'], color=0x00ff00)
        embedkub.add_field(name="You Got:", value=kuboid, inline=False)
        await ctx.send(embed=embedkub)

    @commands.command(description='Coin throw')
    async def monetka(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        mon = random.choice(games.monet)
        embedmonet = discord.Embed(title=STRINGS['other']['cointosstitle'], color=0x00ff00)
        embedmonet.add_field(name="You Got:", value=mon, inline=False)
        await ctx.send(embed=embedmonet)

    @commands.command(description='Casino')
    async def casino(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        kasino1 = random.choice(games.casin_obj1)
        kasino2 = random.choice(games.casin_obj2)
        kasino3 = random.choice(games.casin_obj3)
        embedkas = discord.Embed(title=STRINGS['other']['casinotitle'],color=0x00ff00)
        embedkas.add_field(name=STRINGS['other']['rolled'], value=kasino1, inline=True)
        embedkas.add_field(name=STRINGS['other']['rolled'], value=kasino2, inline=True)
        embedkas.add_field(name=STRINGS['other']['rolled'], value=kasino3, inline=True)
        await ctx.send(embed=embedkas)



def setup(client):
    client.add_cog(minigames(client))
