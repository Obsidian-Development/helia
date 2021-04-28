import asyncio
import discord
from discord_slash import cog_ext, SlashContext
#### PERMISSION ####

def is_admin(member) :
    return member.server_permissions.administrator


#### SAY CHANNELS ####

async def say_gambling(ctx, msg, bot):
    server = ctx.message.server
    channel = await find_or_create_text_channel('gambling', server, bot)
    await bot.send_message(channel, msg)

async def say_general(ctx, msg, bot):
    server = ctx.message.server
    channel = await find_or_create_text_channel('general', server, bot)
    await bot.send_message(channel, msg)

async def say_other(ctx, msg, bot):
    server = ctx.message.server
    channel = await find_or_create_text_channel('other', server, bot)
    await send_message(channel, msg, bot)
    #await bot.send_message(channel, msg)

async def say_music(ctx, msg, bot):
    server = ctx.message.server
    channel = await find_or_create_text_channel('music', server, bot)
    await bot.send_message(channel, msg)

async def say_tax(ctx, msg, bot):
    server = ctx.message.server
    channel = await find_or_create_text_channel('tax', server, bot)
    await bot.send_message(channel, msg, bot)


async def send_message(channel, msg, bot):
    embed = discord.Embed()
    embed.title = "Buffbot"
    embed.description = msg
    embed.color = discord.Color.blue()
    await bot.send_message(channel, "", embed=embed)


async def music_playing(player, bot, server) :
    embed = discord.Embed()
    m, s = divmod(player.duration, 60)
    embed.title = "Music"
    embed.add_field(name="Song name", value=player.title, inline=True)
    embed.add_field(name="Duration", value=str("{}:{}".format(m, s)), inline=True)
    embed.add_field(name="Likes/dislike", value=str(player.likes)+"/"+str(player.dislikes), inline=True)
    embed.add_field(name="Views", value=str(player.views))
    embed.description = "Now playing.. "
    embed.add_field(name="Please add your own music", value="Do !queue <link to song> to queue up a song!")
    embed.color = discord.Color.dark_green()

    channel = await find_or_create_text_channel("music", server, bot)

    await bot.send_message(channel, "", embed=embed)


async def find_or_create_text_channel(name, server, bot) :
    channels = server.channels
    for channel in channels:
        if str(channel.type) == 'text' and channel.name == name :
            return channel
    return await bot.create_channel(name=name, server=server, type='text')


async def find_or_create_voice_channel(name, server, bot):
    channels = server.channels
    for channel in channels:
        if str(channel.type) == 'voice' and channel.name == name:
            return channel
    return await bot.create_channel(name=name, server=server, type='text')