import asyncio
import datetime
import json
import os

import aiohttp
import discord
from discord.ext import commands
from discord_components import (
    Button,
    ComponentsBot,
    DiscordComponents,
    Select,
    SelectOption,
)
from dotenv import load_dotenv

import flwebhost
from listener.core.client import CoreClient
from listener.prefs import Prefs

# from pixivpy_async import PixivClient
# from ytpy import YoutubeClient
# import asyncpraw

prefixes = ["//"]
default_prefix = "//"
server_prefixes = {}
loaded = False
flwebhost.keep_alive()


def load_server_prefixes():
    global server_prefixes

    with open("prefixes.json") as f:
        server_prefixes = json.load(f)


def save_server_prefixes():
    global server_prefixes

    with open("prefixes.json", "w") as fp:
        json.dump(server_prefixes, fp, indent=2)


def get_memory_config():
    intents = discord.Intents.default()
    # Commented line for requesting members privileged intent - uncomment for enabling
    intents.members = True
    # intents.presences = True # Commented line for requesting presence privileged intent - uncomment for enabling
    return intents


def get_prefix(bot, message):
    guild_id = str(message.guild.id)

    if guild_id in server_prefixes:
        return commands.when_mentioned_or(*server_prefixes[guild_id] +
                                          prefixes)(bot, message)

    return commands.when_mentioned_or(*prefixes)(bot, message)


async def main():
    global loop

    # ENVIRONMENTS
    load_dotenv()
    nano_token = os.getenv("BOT_TOKEN")

    # Load server settings
    load_server_prefixes()

    # Configure client
    intents = get_memory_config()
    client = CoreClient(command_prefix=get_prefix, intents=intents)
    client.remove_command("help")

    # Load Dependencies for DI
    session = aiohttp.ClientSession()
    modules = [Prefs(bot=client, server_prefixes=server_prefixes)]
    for command_cog in modules:
        client.add_cog(command_cog)
        print(f"Loaded {command_cog}")
    if __name__ == "__main__":
        # youtube_client = YoutubeClient(session)
        # music_manager = GuildMusicManager(client=client)
        # reddit_client = asyncpraw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
        # client_secret=os.environ['REDDIT_CLIENT_SECRET'],
        # user_agent=os.environ['REDDIT_USER_AGENT'])

        # pixiv_client = PixivClient()

        # Load command Cogs
        startup_extensions = [
            "listener.help",
            "listener.testing",
            "listener.music",
            "listener.moderation",
            "listener.calculator",
            "listener.listeners",
            "listener.admin",
            # 'listener.wallpapers',
            "listener.utilities",
            "listener.gnulinux",
            "listener.general",
            "listener.announce",
            "listener.minigames",
            "listener.other",
            "listener.utils",
            "listener.welcome",
            "listener.goodbye",
            "listener.workers",
            # 'listener.gacha_commands'
        ]
        for extension in startup_extensions:
            try:
                client.load_extension(extension)
                print(f"Loaded {extension}")
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                print("Failed to load extension {}\n{}".format(extension, exc))

    DiscordComponents(client)

    # Run Bot
    try:
        await client.start(nano_token)

    except Exception as e:
        print(e)

    save_server_prefixes()
    print("Saved prefixes")
    await session.close()
    await client.close()
    print("Session closed.")


loop = asyncio.get_event_loop()

loop.run_until_complete(main())
