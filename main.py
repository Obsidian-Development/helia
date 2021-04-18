import discord
import os 
import json
from dotenv import load_dotenv
import asyncio
import sqlite3
from scripts import db
from discord.ext import tasks, commands
from discord_slash import SlashCommand
from slashify import Slashify

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

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
bot = commands.Bot(command_prefix="//", intents=discord.Intents.default())
#intents.members = True # preparation for reenabling welcome and goodbye functionality 
slash = SlashCommand(bot, override_type = True)
Slashify(bot)


#@bot.event
#async def on_message(message):
    #if bot.user.mentioned_in(message) and 'prefix' in message.content:
        #await message.channel.send(f'My Prefix is {bot.command_prefix}')
@tasks.loop(seconds=80)
async def changeStatus():
   while True:
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers "))
    print("Status changed to status 1!")
    await asyncio.sleep(80)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening,name="Dont forget to bump the bot every 3 hours on bot lists!"))
    print("Status changed to status 2!")
    await asyncio.sleep(80)
    await bot.change_presence(activity=discord.Game(name="//help for info"))
    print("Status changed to status 3!")
    await asyncio.sleep(80)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening,name="to my creator Middlle#7488"))
    print("Status changed to status 4!")
    await asyncio.sleep(80)
    await bot.change_presence(activity=discord.Game(name="Final Fantasy XIV"))
    print("Status changed to status 5!")
    await asyncio.sleep(80)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="our support server https://discord.gg/7uUBM8mKbu"))
    print("Status changed to tell about our support server!")
    await asyncio.sleep(80)

@bot.event
async def on_ready():
    db.control()
    print("[SQLITE] Tables checked")
    print("[Коментарий про политику] Надеемся и верим что лукашенку скинут")
    print("[SUCCESS] Started the bot") # Вывод информации о запуске
    changeStatus.start()


bot.remove_command('help')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(TOKEN) # securize token in a .env file 
