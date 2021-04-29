# -*- coding: utf-8 -*-



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
import sqlite3
#from scripts import db
from discord.ext import tasks, commands
from discord_slash import SlashCommand
from slashify import Slashify
import discord



CONFIG = Config()
STRINGS = Strings(CONFIG['default_locale'])

filepath = dirname(abspath(__file__))


cprint(STRINGS['etc']['info']['art'], 'white')

cprint('Default locale is {0}'.format(
    CONFIG['default_locale']), 'green')


bot = AutoShardedBot(command_prefix=Utils.get_prefix, help_command=None)

@tasks.loop(seconds=80)
async def changeStatus():
   """
   Functionality to cycle bot status
   """
   while True:
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers "))
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

    #await bot.change_presence(activity=discord.Game(name='HELIA CANARY BRANCH - INTERNAL TEST ONLY'))
    bot.load_extension('jishaku')
    print("---------------------------")
    print("[SUCCESS] Started Helia discord bot")  # Вывод информации о запуске
    print("---------------------------")
    changeStatus.start()



bot.run(CONFIG['token'])
