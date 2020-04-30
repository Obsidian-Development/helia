import discord
from discord.ext import commands
import os
import aiohttp

class NanoContext(commands.Context):
    @property
    def secret(self):
        return 'this is my secret'

class NanoClient(commands.Bot):
    def __init__(self, name='OpenBot', id='536892183404478483',
        owner_id='213866895806300161', command_prefix='do.'):
        super(NanoClient, self).__init__(command_prefix)
        self.name = name
        self.id = id
        self.owner_id = owner_id
        self.command_prefix = command_prefix
        

    async def update_status_on_dbl(self):
        payload = {"server_count" : len(super(NanoClient, self).guilds)}
        async with aiohttp.ClientSession() as session:
            await session.post(self.BASE_URL, data=payload, headers=self.headers)

    async def on_ready(self):
        status_message = discord.Game("$help , OpenBot")
        await super(NanoClient, self).change_presence(status=discord.Status.online, activity=status_message)
        await self.update_status_on_dbl()
        print("Logged in as {}".format(super(NanoClient, self).user))
    
    async def on_guild_join(self, guild):
        """Updates DBL when client joins a guild"""
        await self.update_status_on_dbl()

    async def on_guild_leave(self, guild):
        """Updates DBL when client leaves a guild"""
        await self.update_status_on_dbl()

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.invoke(await self.get_context(message, cls=NanoContext))
