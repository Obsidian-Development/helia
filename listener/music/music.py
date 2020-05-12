import discord
from discord.ext import commands
from discord.utils import get

import youtube_dl
import asyncio
import os
import json
import time

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'output': r'youtube-dl'
}
ffmpeg_before_opts = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
ffmpeg_options = { #-nostdin
    'options': '-vn'
}

queues = {}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5, ctx):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.id = data.get('id')
        self.duration = data.get('duration')
        self.channel = data.get('uploader')
        self.channel_id = data.get('channel_id')
        self.streaming_from = 'Youtube'
        self.streaming_from_url = 'https://youtube.com'
        self.start_playing = time.time()
        self.resquest_by = ctx.message.author

    @classmethod
    async def from_url(cls, url, *, loop = None, stream = False, ctx):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, before_options=ffmpeg_before_opts), data = data, ctx=ctx)


class Music(commands.Cog):
    def __init__(self,bot):
      self.bot = bot

    @commands.command(pass_context=True, aliases=['j', 'joi', 'entrar', 'conectar', 'c'])
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        

        if not channel:
            if not ctx.author.voice:
                await ctx.send(f'{ctx.message.author.mention}\nYou need to be connected to a voice channel or pass the channel name as a parameter...\n**Ex:** {ctx.prefix}join nomedocanal')
                return
            else:
                channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
            await ctx.send(f'{ctx.message.author.mention},\I am already connected to |{channel}|')
            return

        await channel.connect()
        await ctx.send(f'{ctx.message.author.mention},\connecting to the |{channel}|')

    @commands.command(pass_context=True, aliases=['l', 'disconnect', 'sair', 'desconectar', 'd'])
    async def leave(self, ctx):
       
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'{ctx.message.author.mention},\Disconnecting from the voice channel')
        else:
            await ctx.send(f'Hey {ctx.message.author.mention},\i am not connected to any voice channel currently')

    @commands.command(pass_context=True, aliases=['p', 'tocar', 't'])
    async def play(self, ctx, *, url):
        
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop = self.bot.loop, stream=True, ctx=ctx)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        stitle = str(player.title.replace("[", " ").replace("]", " ")[:44]+"...") if len(player.title) > 45 else player.title
        embed = discord.Embed(
            
            title = '',
            description = f'{ctx.message.author.mention},\nPlaying [{stitle}](https://www.youtube.com/watch?v={player.id}) in *{get(self.bot.voice_clients, guild = ctx.guild).channel}*'
        )
        embed.set_footer(text='Music Service')
        await ctx.message.delete()
        now_playing = await ctx.send(embed = embed)
        await now_playing.add_reaction('⏸️')
        await now_playing.add_reaction('⏹️')
        await now_playing.add_reaction('⏭️')

    @commands.command()
    async def yt(self, ctx, *, url):
        

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, ctx=ctx)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command(pass_context=True, aliases=['pausar'])
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            await ctx.message.add_reaction('⏸️')
            ctx.voice_client.pause()
        else:
            await ctx.send(f'{ctx.message.author.mention},\nNothing playing right now')

    @commands.command(pass_context=True, aliases=['unpause'])
    async def resume(self, ctx):
        
        if ctx.voice_client.is_playing():
            return
        else:
            await ctx.message.add_reaction('⏯️')
            ctx.voice_client.resume()

    @commands.command(pass_context = True, aliases=['parar', 's'])
    async def stop(self, ctx):
        
        await ctx.message.add_reaction('⏹️')
        await ctx.voice_client.disconnect()
    

    @commands.command(name='skip')
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        embed=discord.Embed(title="Music Service", description="Skipping current track")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context = True, aliases=['nowplaying', 'now playing', 'now', 'playing'])
    async def np(self, ctx):
        
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                playing_data = ctx.voice_client.source 
                video_url = f'https://www.youtube.com/watch?v={playing_data.id}'
                video_title = playing_data.title
                stitle = str(video_title.replace("[", " ").replace("]", " ")[:44]+"...") if len(video_title) > 45 else video_title
                streaming_from = playing_data.streaming_from
                streaming_from_url = playing_data.streaming_from_url
                duration = time.strftime('%H:%M:%S', time.gmtime(playing_data.duration)) if playing_data.duration > 3600 else time.strftime('%M:%S', time.gmtime(playing_data.duration))
                channel = 'Video Uploader' if playing_data.channel is None else playing_data.channel
                channel_url = f'https://youtube.com/channel/{playing_data.channel_id}'
                thumbnail = f'https://i.ytimg.com/vi/{playing_data.id}/hqdefault.jpg?'
                resquest_by = playing_data.resquest_by
                current_playing_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - playing_data.start_playing)) if playing_data.duration > 3600 else time.strftime('%M:%S', time.gmtime(time.time() - playing_data.start_playing))
                duration_player_pos = int((time.time() - playing_data.start_playing)/(playing_data.duration/25))
                duration_player_final = ''.join([char*duration_player_pos for char in '▬']) + '⚪' + ''.join([char*(24-duration_player_pos) for char in '▬'])

                embed = discord.Embed(
                    
                    title = '',
                    description = f'{ctx.message.author.mention}\n**Playing started on *{get(self.bot.voice_clients, guild = ctx.guild).channel}*...**\n\nThe track is: [{stitle}]({video_url})\nUploader of the track: [{channel}]({channel_url})\nRequested by: {resquest_by.mention}\n\n{current_playing_time} | {duration}\n{duration_player_final}\n'
                )
                embed.set_footer(text='Music Service')
                embed.set_thumbnail(url=thumbnail)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.delete()
                now_playing = await ctx.send(embed = embed)
                await now_playing.add_reaction('⏸️')
                await now_playing.add_reaction('⏹️')
                await now_playing.add_reaction('⏭️')
            else:
                await ctx.send(f'{ctx.message.author.mention},\nNothing playing currently')
        else:
            await ctx.send(f'{ctx.message.author.mention},\nNot connected to voice channel')

    @commands.command(pass_context = True, aliases = ['vol', 'v'])
    async def volume(self, ctx, *, volume: int):
        
        if volume < 0 or volume > 100:
            await ctx.send(f'{ctx.message.author.mention},\nVolume must be between 0 and 100')
        else:
            ctx.voice_client.source.volume = volume / 100
            await ctx.message.add_reaction('✅')

    @commands.command(pass_context = True, aliases = [''])
    async def loop(self, ctx):
        
        if not ctx.voice_client.is_playing():
            return await ctx.send(f'{ctx.message.author.mention},\nLooping the music')

        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @play.before_invoke
    @yt.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f'{ctx.message.author.mention},\nYou need to be connected to a voice channel!')
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    
def setup(bot):
    bot.add_cog(Music(bot))