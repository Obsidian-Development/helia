import asyncio
import datetime
import itertools
import re
from typing import List, Set, Union

import discord  # type: ignore
from discord.ext import commands  # type: ignore
import wavelink  # type: ignore


RURL = re.compile(r"https?:\/\/(?:www\.)?.+")


class Track(wavelink.Track):
    __slots__ = ("requester", "channel", "message")

    def __init__(self, id_: str, info: dict, *, ctx: commands.Context) -> None:
        super().__init__(id_, info)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.message = ctx.message

    @property
    def is_dead(self) -> bool:
        return self.dead


class Player(wavelink.Player):
    def __init__(
        self,
        bot: Union[commands.Bot, commands.AutoShardedBot],
        guild_id: int,
        node: wavelink.Node,
    ) -> None:
        super(Player, self).__init__(bot, guild_id, node)

        self.queue: asyncio.Queue[Track] = asyncio.Queue()
        self.next_event = asyncio.Event()

        self.volume: int = 40
        self.dj = None
        self.controller_message = None
        self.reaction_task = None
        self.update: bool = False
        self.updating: bool = False
        self.inactive: bool = False

        self.controls = {
            "\N{BLACK RIGHT-POINTING TRIANGLE WITH DOUBLE VERTICAL BAR}": "rp",
            "\N{BLACK SQUARE FOR STOP}": "stop",
            "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}": "skip",
            "\N{TWISTED RIGHTWARDS ARROWS}": "shuffle",
            "\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS WITH CIRCLED ONE OVERLAY}": "repeat",
            "\N{HEAVY PLUS SIGN}": "vol_up",
            "\N{HEAVY MINUS SIGN}": "vol_down",
            "\N{INFORMATION SOURCE}": "queue",
        }

        self.pauses: Set[int] = set()
        self.resumes: Set[int] = set()
        self.stops: Set[int] = set()
        self.shuffles: Set[int] = set()
        self.skips: Set[int] = set()
        self.repeats: Set[int] = set()

        self.eq: str = "Flat"

        bot.loop.create_task(self.player_loop())
        bot.loop.create_task(self.updater())

    @property
    def entries(self) -> List[Track]:
        return list(self.queue._queue)  # type: ignore  # false-positive

    async def updater(self) -> None:
        while not self.bot.is_closed():
            if self.update and not self.updating:
                self.update = False
                await self.invoke_controller()

            await asyncio.sleep(10)

    async def player_loop(self):
        await self.bot.wait_until_ready()

        await self.set_preq("Flat")
        # We can do any pre loop prep here...
        await self.set_volume(self.volume)

        while True:
            self.next_event.clear()

            self.inactive = False

            song = await self.queue.get()
            if not song:
                continue

            self.current = song
            self.paused = False

            await self.play(song)

            # Invoke our controller if we aren't already...
            if not self.update:
                await self.invoke_controller()

            # Wait for TrackEnd event to set our event...
            await self.next_event.wait()

            # Clear votes...
            self.pauses.clear()
            self.resumes.clear()
            self.stops.clear()
            self.shuffles.clear()
            self.skips.clear()
            self.repeats.clear()

    async def invoke_controller(self, track: wavelink.Track = None) -> None:
        """Invoke our controller message, and spawn a reaction controller if one isn't alive."""
        assert self.dj is not None
        if not track:
            track = self.current

        self.updating = True

        embed = discord.Embed(
            title="Music Controller",
            description=(
                f"Now Playing:```ini\n{track.title}\n\n"
                f"[EQ]: {self.eq}\n[Presets]: Flat/Boost/Piano/Metal\n```"
            ),
            colour=0xFFB347,
        )
        embed.set_thumbnail(url=track.thumb)

        if track.is_stream:
            embed.add_field(name="Duration", value="🔴`Streaming`")
        else:
            embed.add_field(
                name="Duration",
                value=str(datetime.timedelta(milliseconds=int(track.length))),
            )
        embed.add_field(name="Video URL", value=f"[Click here!]({track.uri})")
        embed.add_field(name="Requested By", value=track.requester.mention)
        embed.add_field(name="Current Host", value=self.dj.mention)
        embed.add_field(name="Queue Length", value=str(len(self.entries)))
        embed.add_field(name="Volume", value=f"**`{self.volume}%`**")

        if self.entries:
            data = "\n".join(
                f'**-** `{botto.utils.limit_str(t.title, 50)}`\n{"-"*10}'
                for t in itertools.islice(
                    [e for e in self.entries if not e.is_dead], 0, 3, None
                )
            )
            embed.add_field(name="Coming Up:", value=data, inline=False)

        if not await self.is_current_fresh(track.channel) and self.controller_message:
            try:
                await self.controller_message.delete()
            except discord.HTTPException:
                pass

            self.controller_message = await track.channel.send(embed=embed)
        elif not self.controller_message:
            self.controller_message = await track.channel.send(embed=embed)
        else:
            self.updating = False
            await self.controller_message.edit(embed=embed, content=None)
            return

        try:
            self.reaction_task.cancel()
        except AttributeError:
            pass

        self.reaction_task = self.bot.loop.create_task(self.reaction_controller())
        self.updating = False

    async def add_reactions(self) -> None:
        """Add reactions to our controller."""
        assert self.controller_message is not None
        for reaction in self.controls:
            try:
                await self.controller_message.add_reaction(str(reaction))
            except discord.HTTPException:
                return

    async def reaction_controller(self) -> None:
        """Our reaction controller, attached to our controller.
        This handles the reaction buttons and it's controls.
        """
        self.bot.loop.create_task(self.add_reactions())

        def check(r: discord.Reaction, u: discord.User) -> bool:
            if not self.controller_message:
                return False
            if str(r) not in self.controls.keys():
                return False
            if u.id == self.bot.user.id or r.message.id != self.controller_message.id:
                return False
            return u in self.bot.get_channel(int(self.channel_id)).members

        while self.controller_message:
            if self.channel_id is None:
                assert self.reaction_task is not None
                self.reaction_task.cancel()
                return

            reaction, user = await self.bot.wait_for("reaction_add", check=check)
            control = self.controls.get(str(reaction))

            if control == "rp":
                if self.paused:
                    control = "resume"
                else:
                    control = "pause"

            try:
                await self.controller_message.remove_reaction(reaction, user)
            except discord.HTTPException:
                pass
            cmd = self.bot.get_command(control)

            ctx = await self.bot.get_context(reaction.message)
            ctx.author = user

            try:
                if cmd.is_on_cooldown(ctx):
                    pass
                if not await self.invoke_react(cmd, ctx):
                    pass
                else:
                    self.bot.loop.create_task(ctx.invoke(cmd))
            except Exception as e:
                ctx.command = self.bot.get_command("reactcontrol")
                await cmd.dispatch_error(ctx=ctx, error=e)

        await self.destroy_controller()

    async def destroy_controller(self) -> None:
        """Destroy both the main controller and it's reaction controller."""
        try:
            await self.controller_message.delete()  # type: ignore
            self.controller_message = None
        except (AttributeError, discord.HTTPException):
            pass

        try:
            self.reaction_task.cancel()  # type: ignore
        except AttributeError:
            pass

    async def invoke_react(self, cmd: commands.Command, ctx: commands.Context) -> bool:
        if not cmd._buckets.valid:
            return True

        if not await cmd.can_run(ctx):
            return False

        bucket = cmd._buckets.get_bucket(ctx)
        retry_after = bucket.update_rate_limit()
        return not retry_after

    async def is_current_fresh(self, channel: discord.TextChannel) -> bool:
        """Check whether our controller is fresh in message history."""
        try:
            async for m in channel.history(limit=8):
                if m.id == self.controller_message.id:  # type: ignore
                    return True
        except (discord.HTTPException, AttributeError):
            return False
        return False
        
def setup(client):
    client.add_cog(models(client))
