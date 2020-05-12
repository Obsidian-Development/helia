import discord
import os 
import json
import asyncio
import sqlite3
from scripts import db
from discord.ext import commands

startup_extensions = [
    'listener.konsolemod.helper',
    'listener.general_commands',
    'listener.konsolemod.fun',
    'listener.konsolemod.gnulinux',
    'listener.konsolemod.goodbye',
    'listener.konsolemod.infosystem',
    'listener.konsolemod.mod',
    'listener.konsolemod.config',
    #'listener.konsolemod.logs',
    'listener.konsolemod.submits',
    'listener.konsolemod.tickets',
    'listener.konsolemod.welcome',
    'listener.tools',
    'listener.wallpapers',
    'listener.minigames',
    'listener.music.music',
    'listener.announce',
]

# Префикс
def prefixed(bot, message):
    try:
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(db.select_table("prefixes","prefix","guild_id",message.guild.id))
        res = cursor.fetchone()
        cursor.close()
        connect.close()
        if res is None:
            return "$"
        else:
            return res
    except:
        pass   
bot = commands.Bot(command_prefix=prefixed) 

@bot.event
async def on_ready():
    db.control()
    print("[SQLITE] Tables checked")
    print("[SUCCESS] Started the bot") # Вывод информации о запуске
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers ,Openbot"))


bot.remove_command('help')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run("токен ваш")
