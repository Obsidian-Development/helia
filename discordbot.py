import discord
import asyncio
import os
from discord.ext import commands
bot = commands.Bot(command_prefix="$") # Префикс бота


@bot.event
async def on_ready():
    print("[SUCCESS] Бот запущен") # Вывод информации о запуске
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("OpenBot Alive"))

bot.remove_command("help")


@bot.command()
async def shutdown(ctx): # Команда для выключения бота
    author = ctx.message.author
    if author.id == 540142383270985738:
        await ctx.send("Shutting Down The Bot")
        await ctx.bot.logout()
    else:
        await ctx.send("bot: You dont have enough Permissions for this command : Need perms Bot Owner")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="OpenBot", description="Bot imitating linux and unix-like operating systems", color=0x00ff00)
    embed.add_field(name="Author", value="NigamanRPG#6937 for Computer Team , text translated to english by Middlle#7488", inline=False)
    embed.add_field(name="Invite the bot", value="https://discordapp.com/oauth2/authorize?client_id=666304823934844938&scope=bot&permissions=8", inline=True)
    embed.set_footer(text="OpenBot")
    await ctx.send(embed=embed)

@bot.group(invoke_without_command=True) # Команда Help
async def help(ctx): # help
    embed1=discord.Embed(title="OpenBot Commands", description="Info About commands and modules of the bot. Use  help [module] for questions.", color=0x00ff00)
    embed1.add_field(name="moderation", value="Moderation Commands Info.", inline=True)
    embed1.add_field(name="fun [In Development]", value="Information about fun commands.", inline=True)
    embed1.add_field(name="minigames", value="Minigames Info.", inline=True)
    embed1.add_field(name="wallpapers", value="Information about commands providing desktop wallpapers", inline=True)
    embed1.add_field(name="infosystem", value="Information about the commands for obtaining data about the server, user, etc.", inline=True)
    embed1.add_field(name="wiki", value="Wiki Commands.", inline=True)
    embed1.add_field(name="config", value="Command Information for Configuration and Setup.", inline=True)
    embed1.add_field(name="tools", value="Tool Command Information.", inline=True)
    embed1.add_field(name="system", value="Information about the commands for voting, contacting the administration, etc..", inline=True)
    embed1.set_footer(text="OpenBot Help System")
    await ctx.send(embed=embed1)

@help.command(pass_context=True)
async def moderation(ctx):
    modemb = discord.Embed(title="OpenBot. Moderation Module.", description="Moderation Commands", color=0x1fe6ca)
    modemb.add_field(name="devnull [user] {reason} ", value="Ban of the user", inline=False)
    modemb.add_field(name="userdel [user] {reason}", value="Removal of the user", inline=False)
    modemb.add_field(name="rmmod [user] [time] {reason}", value="User Mute", inline=False)
    modemb.add_field(name="unrmmod [user]", value="Unmuting of the user", inline=False)
    modemb.add_field(name="clear [amount]", value="Clearing of messages", inline=False)
    modemb.set_footer(text="OpenBot Help System")
    await ctx.send(embed=modemb)

@help.command(pass_context=True)
async def minigames(ctx):
    mgemb = discord.Embed(title="OpenBot. Minigames Module", description="Minigames Commands", color=0xff9219)
    mgemb.add_field(name="kubik", value="Roll a Cube (result: number from 1 to 6)", inline=False)
    mgemb.add_field(name="monetka", value="Throw a coin (2 results)", inline=False)
    mgemb.add_field(name="casino", value="Play in a casino", inline=False)
    mgemb.set_footer(text="OpenBot Help System")
    await ctx.send(embed=mgemb)

@help.command(pass_context=True)
async def wallpapers(ctx):
    wallemb = discord.Embed(title="OpenBot. Wallpaper Module.", description="Get a desktop wallpaper", color=0xff9219)
    wallemb.add_field(name="wallpaper [category]", value="Get a desktop wallpaper", inline=False)
    wallemb.add_field(name="Categories", value="``anime`` - anime (disgraceful weaboo shit) wallpapers \n ``nature`` - nature wallpapers", inline=False)
    wallemb.set_footer(text="OpenBot Help System")
    await ctx.send(embed=wallemb)

@help.command(pass_context=True)
async def wiki(ctx):
    wikiemb = discord.Embed(title="OpenBot. Wiki Module.", description="Wiki Information Help", color=0xf417ce)
    wikiemb.add_field(name="manjaro", value="Information about a Linux Distribution called Manjaro", inline=False)
    wikiemb.add_field(name="arch", value="Information about a Linux Distribution called Arch", inline=False)
    wikiemb.add_field(name="ubuntu", value="Information about a Linux Distribution called Ubuntu", inline=False)
    wikiemb.add_field(name="mint", value="Information about a Linux Distribution called Linux Mint", inline=False)
    wikiemb.set_footer(text="OpenBot Help System")
    await ctx.send(embed=wikiemb)

@help.command(pass_context=True)
async def infosystem(ctx):
    infemb=discord.Embed(title="OpenBot. Модуль ИнфоСистемы.", description="Commands for obtaining information about the user, server, etc..", color=0x1f8100)
    infemb.add_field(name="neofetch [user]", value="User Information", inline=False)
    infemb.add_field(name="guild ", value="Server Information", inline=False)
    infemb.add_field(name="voicedemo [VoiceChannel]", value="Getting a screen sharing link for a voice chat", inline=False)
    infemb.add_field(name="avatar [user]", value="User Profile Picture", inline=False)
    infemb.set_footer(text="OpenBot Help System")
    await ctx.send(embed=infemb)

@help.command(pass_context=True)
async def config(ctx):
    confemb=discord.Embed(title="OpenBot. Configuration Module", description="Bot Setup Module", color=0x0034f6)
    confemb.add_field(name="welcome channel [TextChannel] | clear", value="Choosing a channel for sending welcome messages | Clearing the configuration file", inline=False)
    confemb.add_field(name="goodbye channel [TextChannel] | clear", value="Choosing a channel to send farewell messages | Clearing the configuration file", inline=False)
    confemb.add_field(name="sub channel [TextChannel] | clear", value="Choosing a channel to send suggestions | Clearing the configuration file", inline=False)
    confemb.add_field(name="ticket channel [TextChannel] | clear", value="Choosing a channel for sending tickets | Clearing the configuration file", inline=False)
    confemb.set_footer(text="OpenBot Help System")
    await ctx.send(embed=confemb)

@help.command(pass_context=True)
async def tools(ctx):
    temb=discord.Embed(title="OpenBot. Tools Module", description="Tool Module Help", color=0x7ba05b)
    temb.add_field(name="randint [Num1] [Num2]", value="Random Number Generator", inline=False)
    temb.add_field(name="sqrt [Num]", value="Display the square root of a specified number", inline=False)
    temb.add_field(name="factorial [Num]", value="Output factorial of a specified number", inline=False)
    temb.add_field(name="embed [Title] [Content]", value="Creating embed with your text", inline=False)
    temb.add_field(name="remind me | role [Time] [Message]", value="Create a reminder for yourself | for the role", inline=False)
    temb.set_footer(text="OpenBot Help System")
    await ctx.send(embed=temb)

@help.command(pass_context=True)
async def system(ctx):
    systememb=discord.Embed(title="OpenBot. System Module", description="Commands for creating suggestions, tickets, etc.", color=0xedf41a)
    systememb.add_field(name="sub create [Text] | faq", value="Create a suggestion | Get the information about reactions and marks", inline=False)
    systememb.add_field(name="ticket create [Text]", value="Creating a support ticket for administration", inline=False)
    systememb.set_footer(text="OpenBot Help System")
    await ctx.send(embed=systememb)


initial_extensions = ["cogs.mod", # Модуль модерации
                      "cogs.minigames", # Модуль мини-игр
                      "cogs.fun", # Модуль фана
                      "cogs.gnulinux", # Модуль wiki
                      "cogs.infosystem", # Модуль инфоСистемы
                      "cogs.goodbye", # Модуль прощальных сообщений
                      "cogs.welcome", # Модуль приветственных сообщений
                      "cogs.tickets", # Модуль тикетов
                      "cogs.submits", # Модуль голосований/предложений
                      "cogs.wallpapers", # Модуль обоев для рабочего стола
                      "cogs.tools"] # Модуль инструментов


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"[OK] Module {extension} loaded fine")
            print("----------------------------------")
        except Exception as e:
            print(f"Module {extension} failed to load")
            raise e


bot.run("ваш токе") # Токен бота для запуска
