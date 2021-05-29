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
#from scripts import db # UNCOMMENT FOR DB CONNECTION
from discord.ext import tasks, commands
from discord_slash import SlashCommand
from slashify import Slashify
import discord



CONFIG = Config()
STRINGS = Strings(CONFIG['default_locale'])

filepath = dirname(abspath(__file__))

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

cprint(STRINGS['etc']['info']['art'], 'white')

cprint('Default locale is {0}'.format(
    CONFIG['default_locale']), 'green')


bot = AutoShardedBot(command_prefix=Utils.get_prefix, help_command=None) # if needed specify ahard_count
intents=discord.Intents.default()
#intents.members = True # preparation for reenabling welcome and goodbye functionality
slash = SlashCommand(bot, override_type = True)
Slashify(bot)


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


@tasks.loop(seconds=80)
async def changeStatus():
   """
   Functionality to cycle bot status
   """
   while True:
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | {len(bot.shards)} shards "))
    print("---------------------------")
    print("Status changed to status 1!")
    print("---------------------------")
    await asyncio.sleep(80)
    await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching,name="Ping me for prefix"))
    print("---------------------------")
    print("Status changed to status 2!")
    print("---------------------------")
    await asyncio.sleep(80)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening,name="Dont forget to bump the bot every 3 hours on bot lists!"))
    print("---------------------------")
    print("Status changed to status 3!")
    print("---------------------------")
    await asyncio.sleep(80)
    await bot.change_presence(activity=discord.Game(name="//help for info"))
    print("---------------------------")
    print("Status changed to status 4!")
    print("---------------------------")
    await asyncio.sleep(80)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening,name="to my creator Middlle#7488"))
    print("---------------------------")
    print("Status changed to status 5!")
    print("---------------------------")
    await asyncio.sleep(80)
    await bot.change_presence(activity=discord.Game(name="Final Fantasy XIV"))
    print("---------------------------")
    print("Status changed to status 6!")
    print("---------------------------")
    await asyncio.sleep(80)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="our support server https://discord.gg/7uUBM8mKbu"))
    print("---------------------------")
    print("Status changed to tell about our support server!(STATUS 7)")
    print("---------------------------")
    await asyncio.sleep(80)
    await bot.change_presence(activity=discord.Game(name="Deep inside, we're nothing more than scions and sinners"))
    print("---------------------------")
    print("Status changed to status 8!")
    print("---------------------------")
    await asyncio.sleep(80)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="headbanging"))
    print("---------------------------")
    print("Status changed to status 9!")
    print("---------------------------")
    await asyncio.sleep(100)

@bot.event
async def on_ready() -> NoReturn:
    for filename in os.listdir(filepath + '/cogs/'):
        if filename.endswith('.py'):
            bot.load_extension('cogs.{0}'.format(filename[:-3]))

    #await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | {len(bot.shards)} shards ")) # static status debug thing
    bot.load_extension('jishaku')
    print("---------------------------")
    print("[SUCCESS] Started Helia discord bot")  # launch information thing
    #print("[DB] Database Present and ready") # DATABASE CONNECT LOG
    print("---------------------------")
    changeStatus.start() # dynamic status starting thing - can be disabled by commenting this line
    #db.control() # UNCOMMENT FOR DB CONNECTION




bot.run(TOKEN) #securize token in a .env - safer compared to storing in config.json
