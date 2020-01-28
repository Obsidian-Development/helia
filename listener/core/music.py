import asyncio
import discord
import youtube_dl
from random import shuffle
from async_timeout import timeout

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -nostats -loglevel 0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.thumbnail = data.get('thumbnail')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        # gonna change this later
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f'{days}d')
        if hours > 0:
            duration.append(f'{hours}h')
        if minutes > 0:
            duration.append(f'{minutes}m')
        if seconds > 0:
            duration.append(f'{seconds}s')

        return ' : '.join(duration)

class GuildVoiceState:
    """Guild voice channel state."""

    def __init__(self, client):
        """Represents every guild state.

        Every guild have their own: client, now_playing song, voice client,
        song queue, volume, search result, channel, skip votes, repeat status.
        """

        self.client = client
        self.current = None # current voice_entry
        self.voice_client = None
        self.queue = [] # voice entries
        self.volume = 0.05
        self.search_result = None
        self.channel = None
        self.skip_votes = set()
        self.repeat = False
        self.waiting = None

    def get_embedded_np(self):
        """Get embbeded 'now playing song'"""

        embed = self.current.create_embed()
        embed.add_field(
            name='Volume',
            value=str(self.volume * 100),
            inline=True
            )
        return embed

    def get_embedded_queue(self):
        """Get embedded current queue state"""

        if self.channel is None:
            embed = discord.Embed(
                title=":x: | Queue is empty.".format(),
                description='Prefix: do. | max_search_limit: 7',
                colour=discord.Colour(value=11735575).orange()
            )
            return embed

        embed = discord.Embed(
            title="{}'s voice state".format(self.channel.guild.name),
            description='Prefix: do. | max_search_limit: 7',
            colour=discord.Colour(value=11735575).orange()
        )

        # Queue state info field
        if self.queue == []:
            fmt_queue='empty'
        else:
            fmt_queue = ''.join(['**{}. {} [{}]**\nRequested by **{}**\n'.format(i + 1, entry.video.title, entry.video.duration, entry.requester) for i, entry in enumerate(self.queue)])
        embed.add_field(
            name=':notes: | Queue',
            value=fmt_queue,
            inline=False)

        ## Repeat status info field
        if self.repeat:
            val_repeat = 'On'
        else:
            val_repeat = 'Off'
        embed.add_field(
            name=':repeat: | Repeat',
            value='**{}**'.format(val_repeat),
            inline=True)

        ## Volumes info field
        if self.volume > 0.5:
            fmt_volume = ':loud_sound: | Volume'
        elif self.volume == 0.0 or self.volume == 0:
            fmt_volume =  ':speaker: | Volume'
        else:
            fmt_volume = ':sound: | Volume'
        embed.add_field(
            name=fmt_volume,
            value='**{}** %'.format(self.volume * 100),
            inline=True)

        # Now playing info field
        if self.current != None:
            fmt_np = '**{}**\nRequested by **{}**'.format(self.current.video.title, self.current.requester)
        else:
            fmt_np = 'None'
        embed.add_field(
            name=':musical_note: | Now playing',
            value=fmt_np,
            inline=False)

        embed.set_thumbnail(url=self.current.player.thumbnail)
        embed.set_footer(
            text='{} can skip current song | {}/3 skip votes.'.format(self.current.requester, str(len(self.skip_votes)) )
            # icon_url=self.client.get_user(self.client.id).avatar_url
        )
        return embed

    def next(self):
        """Trigger after client done playing current song.
        Client get next song to play or if there is no song on queue, client left voice channel.

        State1:
        if theres no any other user (not bot) in voice channel, client leave voice channel.

        State2:
        if queue is empty or theres no next song to play, client leave voice channel.

        State3:
        else, play next song.
        """

        if self.channel is None:
            return

        # check if theres any hooman in voice channel.
        found=False
        for member in self.voice_client.channel.members:
            # found hooman.
            if not member.bot:
                found = True
                break
        # if hooman not found.
        if not found:
            self.skip_votes.clear()
            self.client.loop.create_task(self.done_playing())
            return

        if self.repeat:
            self.queue.append(self.current)

        self.skip_votes.clear()

        if self.queue != []:
            next_entry = self.queue.pop(0)
            future = asyncio.run_coroutine_threadsafe(
                self.get_player(url=next_entry.video.url),
                self.client.loop
                )
            next_entry.player = future.result()
            self.voice_client.play(next_entry.player, after=lambda e: print('Player error: %s' % e) if e else self.next())
            self.voice_client.source.volume = self.volume
            self.current = next_entry
            self.client.loop.create_task(self.notify_np())
        else: # when theres no song to play.. disconnect from voice channel
            self.client.loop.create_task(self.done_playing())

    async def get_player(self, url):
        """Get player from given url."""

        player = await YTDLSource.from_url(
            url,
            loop=self.client.loop,
            stream=True
            )
        return player

    async def notify_np(self):
        """Notify channel about next song"""

        embed = self.get_embedded_np()
        await self.channel.send(embed=embed)

    async def done_playing(self):
        """Trigger when done playing.
        Client immediately left voice channel after done playing song.
        """

        await self.voice_client.disconnect()
        embed = discord.Embed(
            title="Done playing music.",
            colour=discord.Colour(value=11735575).orange()
            )
        await self.channel.send(embed=embed, delete_after=15)

        self.current = None
        self.queue = []

    async def await_for_member(self):
        """Awaiting for any member to join voice channel."""

        await asyncio.sleep(10) # 300
        # if theres no member joins after 5 minutes awaiting
        await self.channel.send(":x: | Left voice channel after 5 minutes afk.", delete_after=15)
        self.channel = None
        self.current = None
        self.queue = []
        await self.voice_client.disconnect()

    def shuffle_queue(self):
        """Shuffles current queue."""

        if self.queue != []:
            shuffle(self.queue)

class VoiceEntry:
    """Entities represents a requested song."""

    def __init__(self, player=None, requester=None, video=None):
        """Attributes.

        player: downloaded instance data to play the song.
        requester: user that requested the song.
        video: youtube video details.
        """

        self.player = player
        self.requester = requester
        self.video = video

    def create_embed(self):
        """Embed for now_playing command."""

        embed = discord.Embed(
            title=':musical_note: Now Playing :musical_note:',
            colour=discord.Colour(value=11735575).orange()
            )
        embed.add_field(
            name='Song',
            value='**{}**'.format(self.player.title),
            inline=False
            )
        embed.add_field(
            name='Requester',
            value=str(self.requester.name),
            inline=True
            )
        embed.add_field(
            name='Duration',
            value=str(self.player.duration),
            inline=True
            )
        if not self.video is None:
            embed.set_thumbnail(url=self.video.thumbnails['high']['url'])
        else:
            embed.set_thumbnail(url=self.player.thumbnail)
        return embed

class AsyncVoiceState:
    """Guild voice channel state that implements asynchronous loop for the audio player task."""

    def __init__(self, client):
        self.client = client
        self.voice_client = None
        self.volume = 0.25
        self.songs = AsyncSongQueue()
        self.asyncio_event = asyncio.Event()
        self.audio_player = client.loop.create_task(self.audio_player_task())

    async def audio_player_task(self):
        while True:
            self.asyncio_event.clear()
            video = await self.songs.get()
            player = await YTDLSource.from_url(video.url, stream=True)
            player.source.volume = self.volume
            self.voice_client.play(player, loop=self.client.loop, after=self.play_next_song)
            await self.asyncio_event.wait()

    def play_next_song(self, error=None):
        fut = asyncio.run_coroutine_threadsafe(self.asyncio_event.set(), self.client.loop)
        try:
            fut.result()
        except:
            print(error + " error")
            pass

class AsyncSongQueue(asyncio.Queue):
    def shuffle(self):
        random.shuffle(self._queue)
