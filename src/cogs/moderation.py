# -*- coding: utf-8 -*-

from typing import NoReturn

import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot, Context

import asyncio

from cogs.utils import Settings, Config, Strings, Utils, Logger


CONFIG = Config()


class Moderation(commands.Cog, name='Moderation'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Moderation'

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx: Context, member: discord.Member, *, reason: str = "N/A") -> NoReturn:
        """Bans the user.

        Attributes:
        -----------
        - `member` - user
        - `reason` - ban reason

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)

        try:
            embed = Utils.error_embed(
                STRINGS['moderation']['dm_ban'].format(ctx.guild.name, reason))
            await member.send(embed=embed)
            await asyncio.sleep(5)
            await member.ban(reason=reason)

        except discord.Forbidden:
            await ctx.message.add_reaction(CONFIG['no_emoji'])
            embed = Utils.error_embed(
                STRINGS['error']['ban_fail'])
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()

        else:
            try:
                embed = Utils.error_embed(
                    STRINGS['moderation']['dm_ban'].format(ctx.guild.name, reason))
                await member.send(embed=embed)
            except:
                pass

            await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unban(self, ctx: Context, *, member: Member) -> NoReturn:
        """Unbans the user.

        Attributes:
        -----------
        - `member` - user tag. Example: `name#1234`

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.message.add_reaction(CONFIG['yes_emoji'])
                return

        await ctx.message.add_reaction(CONFIG['no_emoji'])
        embed = Utils.error_embed(
            STRINGS['error']['user_not_found'])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def multiban(self, ctx: Context, *members: discord.Member) -> NoReturn:
        """Bans multiple users. The reason is "N/A". Maybe I will fix it in the future...

        Attributes:
        -----------
        - `member` - user

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        not_banned_members = []

        for member in members:
            try:
                await member.ban(reason="N/A")
            except discord.Forbidden:
                not_banned_members.append(member.mention)

            else:
                try:
                    embed = Utils.error_embed(
                        STRINGS['moderation']['dm_ban'].format(ctx.guild.name, "N/A"))
                    await member.send(embed=embed)
                except:
                    pass

        if len(not_banned_members) == 0:
            await ctx.message.add_reaction(CONFIG['yes_emoji'])
        else:
            await ctx.message.add_reaction(CONFIG['warn_emoji'])
            msg = await ctx.send(Utils.warn_embed(STRINGS['moderation']['on_not_full_multiban'].format(', '.join(not_banned_members))))
            await asyncio.sleep(10)
            await msg.delete()

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx: Context, member: discord.Member, *, reason: str = "N/A") -> NoReturn:
        """Kicks the user.

        Attributes:
        -----------
        - `member` - user
        - `reason` - kick reason

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)

        embed = Utils.error_embed(
            STRINGS['moderation']['dm_kick'].format(ctx.guild, reason))
        await member.send(embed=embed)
        await asyncio.sleep(5)
        await member.kick()
        await ctx.message.add_reaction(CONFIG['yes_emoji'])



    @commands.command(aliases=['clear'])
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx: Context, number: int) -> NoReturn:
        """Deletes a specified number of messages in the current channel.

        Attributes:
        -----------
        - `number` - The number of messages to be deleted.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)

        deleted = await ctx.channel.purge(limit=number+1)

        embed = Utils.done_embed(
            STRINGS['moderation']['on_clear'].format(len(deleted)))
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await msg.delete()

    @commands.command(aliases=['setnick, setname'])
    @commands.guild_only()
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setname(self, ctx: Context, member: discord.Member, *, name: str) -> NoReturn:
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)

        if len(name) > 32:
            embed = Utils.error_embed(
                STRINGS['error']['too_long_name'])
            await ctx.send(embed=embed)
        else:
            if ctx.message.author.guild_permissions.manage_nicknames or member == ctx.message.author:
                await member.edit(nick=name)
                await ctx.message.add_reaction(CONFIG['yes_emoji'])
            else:
                embed = Utils.error_embed(
                    STRINGS['error']['missing_perms'])
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def mute(self, ctx: Context, member: discord.Member, *, reason: str = "N/A") -> NoReturn:
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        mute_role_id = await s.get_field('mute_role_id')

        if mute_role_id == None or discord.utils.get(ctx.guild.roles, id=mute_role_id) == None:
            embed = Utils.done_embed(
                STRINGS['moderation']['on_mute_role_create'])
            await ctx.send(embed=embed)
            mute_role = await ctx.guild.create_role(name='OpenMod - Muted')

            await s.set_field('mute_role_id', mute_role.id)
            mute_role_id = await s.get_field('mute_role_id')

        else:
            mute_role = discord.utils.get(ctx.guild.roles, id=mute_role_id)

            for user_role in member.roles:
                if user_role == mute_role:
                    embed = Utils.error_embed(
                        STRINGS['error']['already_muted'])
                    await ctx.send(embed=embed)
                    return

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(
                mute_role, read_messages=True, send_messages=False, speak=False)

        await member.add_roles(mute_role)
        await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unmute(self, ctx: Context, member: discord.Member, *, reason: str = "N/A") -> NoReturn:
        mute_role = discord.utils.get(
            ctx.guild.roles, id=Utils.get_mute_role(None, ctx.message))
        if mute_role == None:
            # FIXME
            await ctx.send('нету роли мута ок да\n\n\nок')
        else:
            await member.remove_roles(mute_role)
            await ctx.message.add_reaction(CONFIG['yes_emoji'])


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Moderation(bot))
    Logger.cog_loaded(bot.get_cog('Moderation').name)
