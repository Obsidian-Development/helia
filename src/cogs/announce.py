import asyncio
import os

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from cogs.utils import Config, Logger, Settings, Strings

CONFIG = Config()


class broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Global Announcement from bot owner")
    @commands.is_owner()
    async def announce(self, ctx: SlashContext, *, content):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        prefix = await s.get_field("prefix", CONFIG["default_prefix"])
        STRINGS = Strings(lang)
        announcement = discord.Embed(
            title=STRINGS["general"]["announcestitle"],
            description=STRINGS["general"]["announcesdesc"],
            color=0x3B88C3,
        )
        author_name = f"{ctx.message.author}"
        announcement.set_author(name=author_name, url=ctx.message.author.avatar_url)
        announcement.add_field(
            name=STRINGS["general"]["announcesfieldtitle"],
            value=f"{ctx.message.guild.name}",
            inline=False,
        )
        announcement.add_field(
            name=STRINGS["general"]["announcesfielddesc"], value=content, inline=True
        )
        announcement.set_footer(
            text=STRINGS["general"]["announcesfooter"],
            icon_url=ctx.message.guild.icon_url,
        )
        sent_counter = 0
        text_channel_list = []
        embed = discord.Embed(
            title=STRINGS["general"]["announcestitle"],
            description=STRINGS["general"]["announceaway"],
        )
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

    # @commands.command(description='Debug info')
    # @commands.is_owner()
    # async def debug(self, ctx: SlashContext):
    # voice_states = ctx.bot.voice_clients
    # await ctx.send(f'I am currently in {len(voice_states)} voice channels')


def setup(bot):
    bot.add_cog(broadcast(bot))
    print("Global announcements initialized")
