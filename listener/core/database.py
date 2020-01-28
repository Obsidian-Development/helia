import asyncpg
import random
import json
import discord

class FGOUsers:
    """Entities for users table."""

    def __init__(self):
        """Represents users table attribute."""

        self.id = 0
        self.name = ''
        self.lvl = 0
        self.experience = 0
        self.saint_quartz = 0
        self.join_at = ''
        self.spirit_origin_list = []

    def embed(self):
        """Get embeddded user."""

        embed = discord.Embed(
            title="{}'s Profile'".format(self.name),
            description="Joined at {}".format(self.join_at),
            color=discord.Colour(value=11735575).orange()
            )
        embed.add_field(
            name='Saint Quartz',
            value=self.saint_quartz,
            inline=True
            )
        embed.add_field(
            name='Level',
            value=self.lvl,
            inline=True
            )
        embed.add_field(
            name='Spirit Origin List',
            value=str(self.spirit_origin_list),
            inline=False
            )
        # embed.set_thumbnail(url=avatar_url)
        return embed

class GachaDatabase:
    """FGO Simulator database.
    Table Users:
    user_id         ->  primary key, discord user id.
    username        ->  varchar, discord user's name.
    lvl             ->  integer, user level. note: not yet implemented.
    experience      ->  point for level calculation.
    Saint_Quartz    ->  you know la.
    """

    def __init__(self, client=None):
        self.pg_connection = None
        self.client = client

    async def summon1(self):
        """Simulate 1 times summon."""

        with open('listener/core/nobuDB/gatcha.json', 'r') as f:
            gatcha = json.load(f)

        star = 0
        starRand = random.randint(0, 100)
        servant = True
        # print(starRand)
        if starRand < 1:
            star = 5
        elif starRand <= 3:
            star = 4
        elif starRand <= 43:
            star = 3
        elif starRand <= 47:
            star = 5
            servant = False
        elif starRand <= 59:
            star = 4
            servant = False
        else:
            star = 3
            servant = False

        if servant == True:
            if star == 5:
                id = random.choice(gatcha['servants']['5'])
            elif star == 4:
                id = random.choice(gatcha['servants']['4'])
            else:
                id = random.choice(gatcha['servants']['3'])
            # embed.set_image(url="http://fate-go.cirnopedia.org/icons/servant_card/" + str(id) + "1.jpg")
            # await self.bot.send_message(ctx.message.channel, user.mention, embed=embed)
            with open('listener/core/nobuDB/fgo_main.json', encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
                info = "**[" + data[id]['rarity'] + " Star Servant, " + data[id]['servantClass'] + ", " + data[id]['name'] + "](http://fate-go.cirnopedia.org/icons/servant_card/" + str(id) + "1.jpg)**\n"
                link = "http://fate-go.cirnopedia.org/icons/servant_card/" + str(id) + "1.jpg"
            return ('Servant', info, link)
        else:
            if star == 5:
                id = random.choice(gatcha['ce']['5'])
            elif star == 4:
                id = random.choice(gatcha['ce']['4'])
            else:
                id = random.choice(gatcha['ce']['3'])
            # await self.bot.send_file(ctx.message.channel, "images/CE/" + id + ".png")
            info = ""
            link = "listener/core/nobuDB/images/CE/{}.png".format(id)
            return ('Craft_Essence', info, link)

    async def create_pool(self, db_name='', username='', password=''):
        """Create connection to database."""

        self.pg_connection = await asyncpg.create_pool(
            database=db_name,
            user=username,
            password=password
        )
        return

    async def get_user_by_id(self, id=''):
        """Get user by given id."""

        query = "SELECT * FROM USERS WHERE user_id = '{}'".format(id)
        user = await self.pg_connection.fetch(query)
        return user

    async def create_user(self, id, name):
        """Create new user.
        Primary key: user_id.
        """

        query = """
                    INSERT INTO USERS
                    (user_id, username, lvl, experience, saint_quartz)
                    VALUES('{}','{}', 1, 0, 30)
                """.format(id, name)
        await self.pg_connection.execute(query)
        new_user = await self.get_user_by_id(id=id)
        return new_user

    async def update_quartz(self, id, quartz):
        """Update quartz, can be an increment or decrement."""

        query = """
                    UPDATE USERS
                    SET saint_quartz={}
                    WHERE user_id='{}'
                """.format(quartz, str(id))
        await self.pg_connection.execute(query)
        user = await self.get_user_by_id(id=id)
        return user
