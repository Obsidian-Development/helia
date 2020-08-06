import random
from collections import deque
from .track import Track
import discord


class Queue(deque):
    def __init__(self):
        self.current_message: discord.Message = None
        self.current_track: Track = None
        self._volume = 1.0

    async def after(self):
        self.current_track = None
        await self.current_message.delete()
        self.current_message = None
        await self.next()

    async def next(self):
        """Plays the next track in the queue"""
        if self:
            player = self.popleft()
            await self.play(player)

    async def play(self, player: Track):
        """Plays a track, stops current track if there is one"""
        player.volume = self.volume
        ctx = player.ctx

        self.current_track = player
        if ctx.voice_client is None:
            return
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        ctx.voice_client.play(
            player, after=lambda: ctx.bot.loop.run_until_complete(self.after()))

        embed = discord.Embed(
            title='Now Playing',
            description=f'[{player.title}]({player.webpage_url}) by [{player.uploader}]({player.uploader_url})',
            color=discord.Color.from_rgb(180, 192, 200)) \
            .set_thumbnail(url=player.thumbnail) \
            .add_field(name='Duration', value=player.duration) \
            .set_footer(text=f'Requested by {player.requester.display_name}', icon_url=player.requester.avatar_url)
        self.current_message = await ctx.send(embed=embed)

    def shuffle(self):
        """Shuffles the queue"""
        random.shuffle(self)

    @property
    def volume(self) -> float:
        """Getter for the volume"""
        return self._volume

    @volume.setter
    def volume(self, value: float):
        """Setter for the volume, also sets volume on current track"""
        self._volume = max(0.0, value)
        if self.current_track is not None:
            self.current_track.volume = self.volume
