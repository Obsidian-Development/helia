# -*- coding: utf-8 -*-

from typing import NoReturn

import discord
from discord import Guild, Message
from discord.ext import commands
from discord.ext.commands import Bot, Context

import asyncio
import datetime

from cogs.utils import Logger, Settings, Config, Commands, Strings, Utils


CONFIG = Config()


class Listeners(commands.Cog, name='Listeners'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Listeners'

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild) -> NoReturn:
        """This function sends a welcome message from the bot to the first channel
                in which the bot has the permission to send messages.

        """
        STRINGS = Strings(CONFIG['default_locale'])

        embed = discord.Embed(title=STRINGS['general']['abouttitle'], description=STRINGS['general']['aboutdesc'], color=0xff6900)
        embed.add_field(name=STRINGS['general']['aboutver'], value=ver, inline=True)
        embed.add_field(name=STRINGS['general']['aboutauthoroninvitetitle'],value=STRINGS['general']['aboutauthoroninvite'],inline=True)
        embed.add_field(name=STRINGS['general']['abouthosting'], value=STRINGS['general']['abouthostingvalue'], inline=True)
        #embed.add_field(name=STRINGS['general']['aboutthanks'], value=STRINGS['general']['aboutthankstext'],inline=False)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

    @commands.Cog.listener()
    async def on_command(self, ctx: Context) -> NoReturn:
        """Logging commands to the console.

        """
        Logger.command_used(ctx.message.author,
                            ctx.command.name, ctx.message.guild)

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> NoReturn:
        """Getting the bot prefix when it is mentioned.

        """
        try:
            s = await Settings(message.guild.id)
            lang = await s.get_field('locale', CONFIG['default_locale'])
            prefix = await s.get_field('prefix', CONFIG['default_prefix'])
            STRINGS = Strings(lang)
        except AttributeError:
            pass
        else:
            if message.content == f'<@!{self.bot.user.id}>' or message.content == f'<@{self.bot.user.id}>' or message.content == f'@{self.bot.user}':
                await message.channel.send(STRINGS['etc']['on_mention'].format(message.author.id, prefix))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception) -> NoReturn:
        """If an unexpected error occurs, it displays an... error message?

        Attributes:
        -----------
        - `error` - error information

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        COMMANDS = Commands(lang)

        if isinstance(error, commands.CommandNotFound):
            return
        else:
            await ctx.message.add_reaction(CONFIG['no_emoji'])

            if isinstance(error, commands.MissingRequiredArgument):
                prefix = await s.get_field('prefix', CONFIG['default_prefix'])

                if ctx.command.cog.name != 'Jishaku':
                    embed = Utils.error_embed(STRINGS['etc']['usage']
                                              .format(COMMANDS[ctx.command.cog.name]['commands'][ctx.command.name]['usage']
                                                      .format(prefix)))
                else:
                    pass

            elif isinstance(error, commands.MissingPermissions):
                embed = Utils.error_embed(
                    STRINGS['error']['missing_perms'])

            elif isinstance(error, commands.BotMissingPermissions):
                embed = Utils.error_embed(STRINGS['error']['missing_bot_perms'].format(' '.join(
                    ['+ ' + STRINGS['etc']['permissions'][f'{perm}'] for perm in error.missing_perms])))

            elif isinstance(error, commands.CommandOnCooldown):
                embed = Utils.error_embed(
                    STRINGS['error']['cooldown']
                    .format(error.retry_after))

            else:
                embed = discord.Embed(color=0xdd0000)
                embed.title = STRINGS['error']['on_error_title']
                embed.description = STRINGS['error']['on_error_text'].format(
                    str(error))
                Logger.warn(str(error))

            msg = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await msg.delete()


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Listeners(bot))

    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    Logger.cog_loaded(bot.get_cog('Listeners').name)
