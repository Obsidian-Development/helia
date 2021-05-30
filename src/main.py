# -*- coding: utf-8 -*-
#/********************************************************************************
# * Copyright (c) 2021 Middlle#7488
# *
# * This program and the accompanying materials are made available under the
# * terms of the Eclipse Public License 2.0 which is available at
# * http://www.eclipse.org/legal/epl-2.0, or the Mozilla Public License, Version 2.0
# * which is available at https://www.mozilla.org/en-US/MPL/2.0/
# *
# * SPDX-License-Identifier: EPL-2.0 OR MPL-2.0
# ********************************************************************************/


from typing import NoReturn
from termcolor import cprint

import os

from os.path import dirname
from os.path import abspath

from cogs.utils import Config, Strings, Utils, Logger
from discord.ext import tasks, commands
from discord.ext.commands import AutoShardedBot
import json
from dotenv import load_dotenv
import asyncio
import requests
import sqlite3
# from scripts import db # UNCOMMENT FOR DB CONNECTION
from discord.ext import tasks, commands
from discord_slash import SlashCommand
from slashify import Slashify
import discord
import random

loaded = False

class Helia(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=Utils.get_prefix,
            case_insensitive=True,
            help_command=None,
            intents=discord.Intents.default() # Default intent specified - verified bots will refuse to start with all intents requested.
            # intents.members = True # Commented line for requesting members privileged intent - uncomment for enabling
            # intents.presences = True # Commented line for requesting presence privileged intent - uncomment for enabling
        )

        CONFIG = Config()
        STRINGS = Strings(CONFIG['default_locale'])
        self.filepath = dirname(abspath(__file__))
        self.statuses = [
            discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.guilds)} servers | {len(self.shards)} shards!"),
            discord.Activity(type=discord.ActivityType.watching, name="Ping me for prefix"),
            discord.Activity(type=discord.ActivityType.listening, name="Dont forget to bump the bot every 3 hours on bot lists!"),
            discord.Game(name="//help for info"),
            discord.Activity(type=discord.ActivityType.listening, name="to my creator Middlle#7488"),
            discord.Game(name="Final Fantasy XIV"),
            discord.Activity(type=discord.ActivityType.watching, name="our support server https://discord.gg/7uUBM8mKbu"),
            discord.Game(name="Deep inside, we're nothing more than scions and sinners"),
            discord.Activity(type=discord.ActivityType.watching, name="headbanging")
        ]

        load_dotenv()
        self.TOKEN = os.getenv("DISCORD_TOKEN")

        cprint(STRINGS['etc']['info']['art'], 'white')
        cprint('Default locale is {0}'.format(
            CONFIG['default_locale']), 'green'
        )

        self.slash = SlashCommand(self, override_type=True)
        Slashify(self)
        global loaded

        if not loaded: # using this so the bot doesn't initialize a second time when trying to get variables or functions
            print("Loading cogs:")
            for filename in os.listdir(self.filepath + '/cogs'):
                if filename.endswith('.py'):
                    try:
                        self.load_extension('cogs.{0}'.format(filename[:-3]))
                        print(f"    Loaded '{filename}'")
                    except Exception as e:
                        print(str(e))
            self.load_extension('jishaku')
            print("    Loaded 'jishaku.py'")
            loaded = True

# uncomment the code below if you want to load cogs from folders that are in the cog folder
# this is used too keep things organised and see what belongs to what

#                 elif not "." in filename and os.path.isdir(self.filepath + "/cogs/" + filename):
#                     print(f"    Loading cogs from '{filename}:'")
#                     for filename1 in os.listdir(self.filepath + "/cogs/" + filename):
#                         if filename1.endswith(".py"):
#                             try:
#                                 self.load_extension(f"cogs.{filename}.{filename1}")
#                                 print(f"        Loaded '{filename1}'")
#                             except Exception as e1:
#                                 print(str(e1))

    @tasks.loop(seconds=80)
    async def changeStatus(self):
        await asyncio.sleep(65)
        await self.change_presence(status=discord.Status.online, activity=random.choice(self.statuses))

    async def on_connect(self):
        print("[CONNECTION] Connected to the Discord API")

    async def on_ready(self):
        print("---------------------------")
        print("[SUCCESS] Started Helia Discord bot")  # launch information thing
        # print("[DB] Database Present and ready") # DATABASE CONNECT LOG
        print("---------------------------")
        self.changeStatus.start() # dynamic status starting thing - can be disabled by commenting this line
        # db.control() # UNCOMMENT FOR DB CONNECTION

def add_to_guild(access_token, userID):
    url = f"{Oauth.discord_api_url}/guilds/{816985615811608616}/members/{userID}"
    headers = {
        "Authorization" : f"Bot {access_token}",
        'Content-Type': 'application/json'
    }

    data = {
        "access_token" : access_token
    }

    response = requests.put(url=url, json=data, headers=headers)
    print(response.text)

if __name__ == "__main__":
    bot = Helia()
    bot.run(bot.TOKEN) #securize token in a .env - safer compared to storing in config.json
