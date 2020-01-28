import discord
from discord.ext import commands
from .core.database import GachaDatabase
from .core import config

class GachaListener:
    """FGO simulator commands listener."""

    def __init__(self, client):
        self.client = client
        self.database = GachaDatabase(client=client)
        self.client.loop.create_task(
            self.database.create_pool(
                db_name='NanoRewrite',
                username='postgres',
                password=config.PG_PASSWORD
                )
            )

    async def get_user(self, id):
        """Get user by id."""
        
        user_id = str(id)
        user = await self.database.get_user_by_id(user_id)
        if not user:
            user = await self.database.create_user(
                id=user_id,
                name=ctx.author.name
            )
        return user

    @staticmethod
    def get_embedded_user(user, avatar_url=''):
        embed = discord.Embed(
            title="{}'s Profile'".format(user[0]['username']),
            description="Joined at {}".format(user[0]['join_at']),
            color=discord.Colour(value=11735575).orange()
            )
        embed.add_field(
            name='Saint Quartz',
            value=user[0]['saint_quartz'],
            inline=True
            )
        embed.add_field(
            name='Level',
            value=user[0]['lvl'],
            inline=True
            )
        embed.add_field(
            name='Spirit Origin List',
            value=str(user[0]['spirit_origin_list']),
            inline=False
            )
        embed.set_thumbnail(url=avatar_url)
        return embed

    @commands.command(name='charge')
    async def charge_(self, ctx, player : discord.User, sq : int):
        """Recharge saint quartz"""

        if ctx.author.id != 213866895806300161:
            return
        user_id = str(player.id)
        user = await self.get_user(user_id)
        user = await self.database.update_quartz(
            id=user_id, quartz=user[0][4] + sq
            )
        embed = self.get_embedded_user(user, avatar_url=player.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='daily', aliases=['Daily', 'claim_daily'])
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def daily(self, ctx):
        """Claim daily rewards, 3 quartz"""

        user_id = str(ctx.author.id)
        user = await self.database.get_user_by_id(user_id)
        if not user:
            user = await self.database.create_user(
                id=user_id,
                name=ctx.author.name
            )
        user = await self.database.update_quartz(id=user_id, quartz=user[0][4] + 3)
        # send embed
        embed = self.get_embedded_user(user, avatar_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='roll1', aliases=['roll', 'roll_1'])
    async def roll_(self, ctx):
        """Summon spirit origin list one time"""

        user = await self.database.get_user_by_id(ctx.author.id)
        if not user:
            user = await self.database.create_user(
                id=str(ctx.author.id),
                name=ctx.author.name
            )
        elif user[0]['saint_quartz'] < 3:
            await ctx.send('{} Need at least 3 quartz to summon 1'.format(ctx.author.mention))
            return
        user = await self.database.update_quartz(
            id=str(ctx.author.id),
            quartz=user[0]['saint_quartz'] - 3
            )
        spirit_origin = await self.database.summon1()

        if spirit_origin[0] == 'Servant':
            embed = discord.Embed(
                title="{}".format(spirit_origin[1]),
                colour=discord.Colour(value=11735575).orange()
            )
            embed.set_image(url=spirit_origin[2])
            await ctx.send(embed=embed)
        else:
            await ctx.send('{}'.format(ctx.author.mention), file=discord.File(spirit_origin[2]))

def setup(client):
    client.add_cog(GachaListener(client))
    print('GachaListener is loaded')
