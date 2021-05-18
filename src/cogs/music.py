# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from enum import Enum
import typing as t
import wavelink
import asyncio
import random
import re
from cogs.utils import Logger, Settings, Config, Commands, Strings, Utils
#from logging_files.music_log import logger

CONFIG = Config()

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

OPTIONS = {
    "1️⃣": 1,"2️⃣": 2,"3️⃣": 3,"4️⃣": 4,"5️⃣": 5,
}

class AlreadyConnectedToChannel(commands.CommandError):
    pass

class NoVoiceChannel(commands.CommandError):
    pass

class QueueIsEmpty(commands.CommandError):
    pass

class NoTracksFound(commands.CommandError):
    pass

class PlayerIsAlreadyPaused(commands.CommandError):
    pass

class PlayerIsAlreadyPlaying(commands.CommandError):
    pass

class NoMoreTracks(commands.CommandError):
    pass

class NoPreviousTracks(commands.CommandError):
    pass

class InvalidRepeatMode(commands.CommandError):
    pass

class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2

class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty
        self.position += 1
        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None
        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty
        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "noloop":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "onesong":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "entirequeue":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0

class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel
        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        if not tracks:
            raise NoTracksFound
        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
            playEmbedplaylist = discord.Embed(title=STRINGS['music']['embed_controler_title'], description=STRINGS['music']['embed_controler_desc'], color=0xff8000)
            playEmbedplaylist.add_field(name=STRINGS['music']['embed_controler_playlistadd'], value=STRINGS['music']['embed_controler_playlistadddesc'],inline=True)
            playEmbedplaylist.add_field(name=STRINGS['music']['embed_controler_req'], value=f"{ctx.author}", inline=True)
            playEmbedplaylist.set_footer(text=STRINGS['music']['embed_controler_footer'])

            await ctx.send(embed=playEmbedplaylist)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            playEmbed = discord.Embed(title=STRINGS['music']['embed_controler_title'], description=STRINGS['music']['embed_controler_desc'], color=0xff8000)
            playEmbed.add_field(name=STRINGS['music']['embed_controler_secdesc'], value=f"{tracks[0].title}", inline=True)
            playEmbed.add_field(name=STRINGS['music']['embed_controler_dur'], value=f"**({tracks[0].length//60000}:{str(tracks[0].length%60).zfill(2)})**",inline=True)
            playEmbed.add_field(name=STRINGS['music']['embed_controler_req'], value=f"{ctx.author}", inline=True)
            playEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])

            await ctx.send(embed=playEmbed)

            #logger.info(f"[MUSIC]Tracks added by {ctx.author} in {ctx.message.guild}")
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                playEmbed_2 = discord.Embed(title=STRINGS['music']['embed_controler_title'],description=STRINGS['music']['embed_controler_desc'], color=0xff8000)
                playEmbed_2.add_field(name=STRINGS['music']['embed_controler_secdesc'], value=f"{tracks[0].title}",inline=True)
                playEmbed_2.add_field(name=STRINGS['music']['embed_controler_dur'],value=f"**({tracks[0].length // 60000}:{str(tracks[0].length % 60).zfill(2)})**",inline=True)
                playEmbed_2.add_field(name=STRINGS['music']['embed_controler_req'], value=f"{ctx.author}", inline=True)
                playEmbed_2.set_footer(text=STRINGS['music']['embed_controler_footer'])
                await ctx.message.delete()

                await ctx.send(embed=playEmbed_2)

                #logger.info(f"[MUSIC]Tracks added by {ctx.author} in {ctx.message.guild}")
        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        chooseTrackEmbed = discord.Embed(description=("\n".join(f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"for i, t in enumerate(tracks[:5]))),colour=0xffd500,timestamp=ctx.message.created_at)
        chooseTrackEmbed.set_author(name=STRINGS['music']['embed_controler_searchresults'])
        chooseTrackEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])
        msg = await ctx.send(embed=chooseTrackEmbed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)

class Music(commands.Cog, wavelink.WavelinkMixin, name='Music'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Music'
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await print(f"Someone left voice chat in {self.ctx.message.guild}")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        nodes = {
            "MAIN": {
                "host": "heroku-lavalink-heliaservice.herokuapp.com",
                "port": 80,
                "rest_uri": "https://heroku-lavalink-heliaservice.herokuapp.com",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "us",
            }
        }
        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)
    @commands.command(name="leave", brief = "L.",aliases=["fuck_off","buggerout","disconnect","lv","пшелвон","fuckoff","отключиться"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()

        #logger.info(f"[MUSIC]Voice channel quit requested by {ctx.author} in {ctx.message.guild}")

    @commands.command(name="play", brief = "play music.",aliases=["p","pl","игратьмузыку"])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        player = self.get_player(ctx)
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        if not player.is_connected:
            await player.connect(ctx)

        if query is None:

            if player.queue.is_empty:
                raise QueueIsEmpty
            elif player.is_paused :
                await player.set_pause(False)
                playEmbed=discord.Embed(title=STRINGS['music']['playresume'],colour=0xffd500)
                playEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])

                await ctx.send(embed=playEmbed)
            else:
                raise PlayerIsAlreadyPlaying
        else:
            query = query.strip("<>")

            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPlaying):
            playEmbed_2=discord.Embed(title=STRINGS['music']['playererrorone'],colour=0xffd500)
            await ctx.send(embed=playEmbed_2)
        elif isinstance(exc, QueueIsEmpty):
            s = await Settings(ctx.guild.id)
            lang = await s.get_field('locale', CONFIG['default_locale'])
            STRINGS = Strings(lang)
            playEmbed_3=discord.Embed(title=STRINGS['music']['queueerror'],description=STRINGS['music']['queueerrordesc'],colour=0xffd500)
            playEmbed_3.set_footer(text=STRINGS['music']['embed_controler_footer'])
            await ctx.send(embed=playEmbed_3)

    @commands.command(name="pause", brief = "Pause playback.",aliases=["ps","pauza","пауза"])
    async def pause_command(self, ctx):
        player = self.get_player(ctx)
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        if player.is_paused:
            raise PlayerIsAlreadyPaused
        await player.set_pause(True)
        pauseEmbed=discord.Embed(title=STRINGS['music']['pausetracktext'],colour=0xffd500)
        pauseEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])

        await ctx.send(embed=pauseEmbed)

        #logger.info(f"[MUSIC]Music paused by {ctx.author} in {ctx.message.guild}")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            pauseer_embed=discord.Embed(title=STRINGS['music']['pauseerror'],colour=0xffd500)
            await ctx.send(embed=pauseer_embed)

    @commands.command(name="stop", brief = "Stops music playback.",aliases=["sp","стоп"])
    async def stop_command(self, ctx):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        stopEmbed=discord.Embed(title=STRINGS['music']['stoptext'],colour=0xffd500)
        stopEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])

        await ctx.send(embed=stopEmbed)

        #logger.info(f"[MUSIC]Music stopped by {ctx.author} in {ctx.message.guild}")

    @commands.command(name="skip", brief = "Skips currently playing song.",aliases=["next","s","скип"])
    async def next_command(self, ctx):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks
        await player.stop()
        nextEmbed=discord.Embed(title=STRINGS['music']['skipsongtext'],colour=0xffd500)
        if upcoming := player.queue.upcoming:
            nextEmbed.add_field(name=STRINGS['music']['queuenextinline'],value=("\n".join(f"**{i + 2}.** {t.title}" for i, t in enumerate(upcoming[:19]))),inline=False)
        nextEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])

        await ctx.send(embed=nextEmbed)

        #logger.info(f"[MUSIC]Next song requested by {ctx.author} in {ctx.message.guild}")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            s = await Settings(ctx.guild.id)
            lang = await s.get_field('locale', CONFIG['default_locale'])
            STRINGS = Strings(lang)
            nextEmbed_2=discord.Embed(title=STRINGS['music']['queueerror'],description=STRINGS['music']['queueerrordesc'],colour=0xffd500)
            nextEmbed_2.set_footer(text=STRINGS['music']['embed_controler_footer'])
            await ctx.send(embed=nextEmbed_2)
        elif isinstance(exc, NoMoreTracks):
            s = await Settings(ctx.guild.id)
            lang = await s.get_field('locale', CONFIG['default_locale'])
            STRINGS = Strings(lang)
            nextEmbed_3=discord.Embed(title=STRINGS['music']['nomoretrackstext'],description=STRINGS['music']['nomoretrackdesc'],colour=0xffd500)
            nextEmbed_3.set_footer(text=STRINGS['music']['embed_controler_footer'])
            await ctx.send(embed=nextEmbed_3)

    @commands.command(name="previous", brief = "Returns to the previous song in the list.",aliases=["prev","предыдущая"])
    async def previous_command(self, ctx):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        player = self.get_player(ctx)
        if not player.queue.history:
            raise NoPreviousTracks
        player.queue.position -= 2
        await player.stop()
        previousEmbed=discord.Embed(title="Listedeki mevcut sıradan bir önceki parça çalınıyor.",colour=0xffd500)
        previousEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=previousEmbed)

        #logger.info(f"[MUSIC]Previous song requested by {ctx.author} in {ctx.message.guild}")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            s = await Settings(ctx.guild.id)
            lang = await s.get_field('locale', CONFIG['default_locale'])
            STRINGS = Strings(lang)
            previousEmbed_2=discord.Embed(title=STRINGS['music']['queueerror'],description=STRINGS['music']['queueerrordesc'],colour=0xffd500)
            previousEmbed_2.set_footer(text=STRINGS['music']['embed_controler_footer'])
            await ctx.send(embed=previousEmbed_2)
        elif isinstance(exc, NoPreviousTracks):
            previousEmbed_3=discord.Embed(title=STRINGS['music']['nomoretrackstext'],description=STRINGS['music']['nomoretracksprevdesc'],colour=0xffd500)
            previousEmbed_3.set_footer(text=STRINGS['music']['embed_controler_footer'])
            await ctx.send(embed=previousEmbed_3)

    @commands.command(name="shuffle", brief = "Shuffles queue.",aliases=["randomize","рандомизацияплейлиста"])
    async def shuffle_command(self, ctx):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        player = self.get_player(ctx)
        player.queue.shuffle()
        shuffleEmbed=discord.Embed(title=STRINGS['music']['listshuffled'],colour=0xffd500)
        shuffleEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])

        await ctx.send(embed=shuffleEmbed)

        #logger.info(f"[MUSIC]Playlist shuffle requested by {ctx.author} in {ctx.message.guild}")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            s = await Settings(ctx.guild.id)
            lang = await s.get_field('locale', CONFIG['default_locale'])
            STRINGS = Strings(lang)
            shuffleEmbed_2=discord.Embed(title=STRINGS['music']['queueerror'],description=STRINGS['music']['queueerrordesc'],colour=0xffd500)
            shuffleEmbed_2.set_footer(text=STRINGS['music']['embed_controler_footer'])
            await ctx.send(embed=shuffleEmbed_2)

    @commands.command(name="queue", brief = "Lists the songs in queue.",aliases=["q","ochered","очередь"])
    async def queue_command(self, ctx):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty
        queueEmbed = discord.Embed(title=STRINGS['music']['queuelisttext'],colour=0xffd500)
        queueEmbed.add_field(name=STRINGS['music']['queuelistcurrentlyplaying'], value=player.queue.current_track.title, inline=False)

        if upcoming := player.queue.upcoming:
            queueEmbed.add_field(name=STRINGS['music']['queuenextinline'],value=("\n".join(f"**{i+2}.** {t.title}"for i, t in enumerate(upcoming[:19]))),inline=False)
        queueEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])

        await ctx.send(embed=queueEmbed)

        #logger.info(f"[MUSIC]Queue requested by {ctx.author} in {ctx.message.guild}")

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            s = await Settings(ctx.guild.id)
            lang = await s.get_field('locale', CONFIG['default_locale'])
            STRINGS = Strings(lang)
            queueEmbed_2=discord.Embed(title=STRINGS['music']['queueerror'],description=STRINGS['music']['queueerrordesc'],colour=0xffd500)
            queueEmbed_2.set_footer(text=STRINGS['music']['embed_controler_footer'])
            await ctx.send(embed=queueEmbed_2)

    @commands.command(name="volume", brief = "Sets bot volume.",aliases=["vol","громкость"])
    async def volume_command(self,ctx,value:int):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty
        if not 0 < value < 101:
            volumeEmbed_3 = discord.Embed(title=STRINGS['music']['invalidvolumevalue'], description=STRINGS['music']['invalidvolumevaluedesc'],colour=0xffd500)
            return await ctx.send(embed=volumeEmbed_3)

        await player.set_volume(value)
        volumeEmbed=discord.Embed(title=STRINGS['music']['volumeset'], description=STRINGS['music']['volumesetdesc'], color=0xff8040)
        volumeEmbed.add_field(name=STRINGS['music']['volumesetvalue'], value=f"{value} ", inline=True)
        volumeEmbed.set_footer(text=STRINGS['music']['embed_controler_footer'])

        await ctx.send(embed=volumeEmbed)

        #logger.info(f"[MUSIC]Volume change requested by {ctx.author} in {ctx.message.guild}")

    @volume_command.error
    async def volume_command_error(self,ctx,exc):
        if isinstance(exc, QueueIsEmpty):
            s = await Settings(ctx.guild.id)
            lang = await s.get_field('locale', CONFIG['default_locale'])
            STRINGS = Strings(lang)
            volumeEmbed_2=discord.Embed(title=STRINGS['music']['queueerror'],description=STRINGS['music']['queueerrordesc'],colour=0xffd500)
            volumeEmbed_2.set_footer(text=STRINGS['music']['embed_controler_footer'])
            await ctx.send(embed=volumeEmbed_2)

def setup(bot):
    bot.add_cog(Music(bot))
    Logger.cog_loaded(bot.get_cog('Music').name)
