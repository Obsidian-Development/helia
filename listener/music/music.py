from .queue import Queue
import typing
from collections import defaultdict
from discord.ext import commands
import youtube_dl
import re
import discord
from .track import Track

URL_REGEX = r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'


class Logger(object):
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'cache/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilename': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'logger': Logger()
}
ytdl = youtube_dl.YoutubeDL(ytdl_options)


class Music(commands.Cog):
    def __init__(self):
        self._queues = defaultdict(Queue)

    def _queue(self, ctx: commands.Context):
        return self._queues[ctx.guild.id]

    def _extract_info(self, url: str, ctx: commands.Context):
        info = ytdl.extract_info(url, download=False)
        if info['extractor'] == 'youtube:search':
            info = info['entries'][0]
        if 'entries' in info:
            return map(lambda t: Track(t, ctx, self._queue(ctx).volume), info['entries'])
        else:
            return [Track(info, ctx, self._queue(ctx).volume)]

    @commands.command(aliases=['join', 'summon'])
    @commands.guild_only()
    async def connect(self, ctx: commands.Context, *, channel: typing.Optional[discord.VoiceChannel]):
        """Joins a voice channel or moves to another one"""
        if channel is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
            else:
                await ctx.send(':x: **You are not connected to a voice channel**', delete_after=5)
                return

        if ctx.voice_client is not None:
            if channel == ctx.voice_client.channel:
                await ctx.send(f':x: **I am already in `{channel}`**', delete_after=5)
                return

            await ctx.voice_client.move_to(channel)
            await ctx.send(f':white_check_mark: **Moved to `{channel}`**', delete_after=5)
        else:
            await channel.connect()
            await ctx.send(f':white_check_mark: **Joined `{channel}`**', delete_after=5)

        await self._queue(ctx).next()

    @commands.command(aliases=['leave'])
    @commands.guild_only()
    async def disconnect(self, ctx: commands.Context):
        """Stops playback and leaves the channel"""
        if ctx.voice_client is None:
            await ctx.send(f':x: **I am not connected to a voice channel**', delete_after=5)
            return

        channel = ctx.voice_client.channel

        await ctx.voice_client.disconnect()
        await ctx.send(f':white_check_mark: **Disconnected from `{channel}`**', delete_after=5)

    @commands.command()
    @commands.guild_only()
    async def play(self, ctx: commands.Context, *, url: str):
        """Plays the url or adds it to the queue"""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(':x: **I am not connected to a voice channel**', delete_after=5)
                return

        msg = await ctx.send(f'**Searching** :mag_right: `{url}`')
        first, *rest = self._extract_info(url, ctx)
 
        if ctx.bot.config.get('delete_messages'):
            await ctx.channel.delete_messages([ctx.message, msg])
        if not ctx.voice_client.is_playing():
            await self._queue(ctx).play(first)
        else:
            self._queue(ctx).append(first)
            embed = discord.Embed(
                title='Added to queue',
                description=f'[{first.title}]({first.webpage_url}) by [{first.uploader}]({first.uploader_url})',
                color=discord.Color.from_rgb(180, 192, 200)) \
                .set_thumbnail(url=first.thumbnail) \
                .add_field(name='Duration', value=first.duration)
            await ctx.send(embed=embed, delete_after=5)
        if rest:
            self._queue(ctx).extend(rest)

    @commands.command()
    @commands.guild_only()
    async def queue(self, ctx: commands.Context):
        """Shows which songs are queued at the moment"""
        embed = discord.Embed(
            title=f'Queue for {ctx.guild}',
            color=discord.Color.from_rgb(180, 192, 200))

        if self._queue(ctx):
            next_songs = ''
            for index, player in enumerate(self._queue(ctx)):
                next_songs += f'{index + 1}. [{player.title}]({player.webpage_url}) by [{player.uploader}]({player.uploader_url}) ({player.duration})\n'
            embed.add_field(name='Next songs', value=next_songs)
        else:
            embed.description = 'No songs in the queue'

        await ctx.send(embed=embed, delete_after=5)


def setup(bot):
    bot.add_cog(Music())
