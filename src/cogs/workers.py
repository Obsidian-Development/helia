# -*- coding: utf-8 -*-

from typing import NoReturn

from discord.ext import commands
from discord.ext.commands import Bot

import asyncio
import requests

from cogs.utils import Config, Logger


CONFIG = Config()


class Workers(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Workers'
        bot.loop.create_task(Workers.sdc_updater(self, bot))

    async def sdc_updater(self, bot: Bot) -> NoReturn:
        """Updates bot information on bots.servers-discord.com

        """
        while True:
            requests.post(f'https://api.server-discord.com/v2/bots/{bot.user.id}/stats',
                          headers={
                              "Authorization": CONFIG['sdc_token']},
                          data={"servers": len(bot.guilds), "shards": 0})
            await asyncio.sleep(3600)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Workers(bot))
    Logger.cog_loaded(bot.get_cog('Workers').name)
