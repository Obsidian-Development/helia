import asyncio
import os
import random

import aiohttp
import discord
from discord.ext import commands, tasks


class NanoContext(commands.Context):
    @property
    def secret(self):
        return "this is my secret"


class CoreClient(commands.AutoShardedBot):
    def __init__(self,
                 name="Helia",
                 id=536892183404478483,
                 command_prefix="n>",
                 intents=None):
        super(CoreClient, self).__init__(
            command_prefix=command_prefix,
            max_messages=None,
            intents=intents,
            chunk_guilds_at_startup=False,
        )
        self.name = name
        self.id = id
        self.command_prefix = command_prefix

        # Discord Bot List updates.
        # self.dbl_token = os.environ['DBL_TOKEN']
        # self.BASE_URL = "https://discordbots.org/api/bots/458298539517411328/stats"
        # self.headers = {"Authorization": self.dbl_token}

    @tasks.loop(seconds=80)
    async def changeStatus(self):
        statuses = [
            # discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.guilds)} servers | {len(self.bot.shards)} shards!"), # bugged status - uncomment after fix
            discord.Activity(type=discord.ActivityType.watching,
                             name="Ping me for prefix"),
            discord.Activity(
                type=discord.ActivityType.listening,
                name="Dont forget to bump the bot every 3 hours on bot lists!",
            ),
            # discord.Game(name=f"{command_prefix}help for info"),
            discord.Activity(type=discord.ActivityType.listening,
                             name="to my creator Middlle#7488"),
            discord.Game(name="Final Fantasy XIV"),
            discord.Activity(
                type=discord.ActivityType.watching,
                name="our support server https://discord.gg/7uUBM8mKbu",
            ),
            discord.Game(
                name="Deep inside, we're nothing more than scions and sinners"
            ),
            discord.Activity(type=discord.ActivityType.watching,
                             name="headbanging"),
        ]
        await asyncio.sleep(40)
        print("---------------------------")
        print("[DYNAMIC-STATUS] Dynamic status changed")
        print("---------------------------")
        await self.change_presence(status=discord.Status.online,
                                   activity=random.choice(statuses))

    async def update_status_on_dbl(self):
        payload = {"server_count": len(super(CoreClient, self).guilds)}
        async with aiohttp.ClientSession() as session:
            await session.post(self.BASE_URL,
                               data=payload,
                               headers=self.headers)

    async def on_ready(self):
        self.changeStatus.start()
        self.load_extension("jishaku")
        print("    Loaded 'jishaku.py'")
        await super(CoreClient,
                    self).change_presence(status=discord.Status.online)
        # await self.update_status_on_dbl()
        print("Logged in as {}".format(super(CoreClient, self).user))

        # async def on_guild_join(self, guild):
        """Updates DBL when client joins a guild"""
        # await self.update_status_on_dbl()

    async def on_guild_leave(self, guild):
        """Updates DBL when client leaves a guild"""
        # await self.update_status_on_dbl()

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.invoke(await self.get_context(message, cls=NanoContext))
