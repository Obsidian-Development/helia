import discord
import os 
import json
import asyncio
import sqlite3
from scripts import db
from discord.ext import commands
from discord_slash import SlashCommand


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
#def prefixed(bot, message):
    #try:
        #connect = sqlite3.connect(db.main)
        #cursor = connect.cursor()
        #cursor.execute(db.select_table("prefixes","prefix","guild_id",message.guild.id))
        #res = cursor.fetchone()
        #cursor.close()
        #connect.close()
        #if res is None:
            #return "$"
        #else:
            #return res
    #except:
        #pass   
bot = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, auto_register=True)

#@bot.event
#async def on_message(message):
    #if bot.user.mentioned_in(message) and 'prefix' in message.content:
        #await message.channel.send(f'My Prefix is {bot.command_prefix}')

@bot.event
async def on_ready():
    db.control()
    print("[SQLITE] Tables checked")
    print("[Коментарий про политику] Надеемся и верим что лукашенку скинут")
    print("[SUCCESS] Started the bot") # Вывод информации о запуске
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers "))


bot.remove_command('help')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run("сами создавайте на discord.com/developers")
