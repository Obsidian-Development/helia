import discord
from discord.ext import commands
import datetime
import re
import asyncio


class timedelta(datetime.timedelta):
    def __str__(self):
        return re.sub(r'^0:', '', super().__str__(), 1)


class Track(discord.PCMVolumeTransformer):
    def __init__(self, data: dict, ctx: commands.Context, volume: float = 1.0):
        super().__init__(discord.FFmpegPCMAudio(data.get('url')), volume)

        self.ctx = ctx
        self.data = data

        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.duration = timedelta(seconds=int(data.get('duration')))
        self.webpage_url = data.get('webpage_url')
        self.url = data.get('url')
        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')

    @property
    def requester(self):
        return self.ctx.author
