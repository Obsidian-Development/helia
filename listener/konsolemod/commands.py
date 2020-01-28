import hashlib
import math
import os
import random

import aiohttp
from discord.ext import commands
from simpleeval import simple_eval

import global_methods
from db import database


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.player = None
        self.volume = 1.0
        self.database = database.Database()

    @commands.command(name="bye", pass_context=True)
    async def bye(self, ctx):
        if not global_methods.is_admin(ctx.message.author):
            await self.bot.say("You're not a big boy")
            return None

        await self.bot.say("Bye bye!")
        await self.bot.logout()

    @commands.command(name="math", pass_context=True)
    async def math(self, ctx, *, params):
        try:
            result = simple_eval("{}".format(params), names={"e": math.e, "pi": math.pi},
                                 functions={"log": math.log, "sqrt": math.sqrt, "cos": math.cos, "sin": math.sin,
                                            "tan": math.tan})
        except Exception:
            result = "Read the fucking manual"

        await self.respond(result, ctx.message.author.mention)

    @commands.command(name="doStuff", pass_context=True)
    async def do_stuff(self, ctx):
        pass

    @commands.command(name="8ball", help="you may or may not get a yes or a no answer")
    async def eightball(self):
        await self.bot.say(get_random_line('8ballresponses.txt'))

    @commands.command(name="whoIsTheBuffest", pass_context=True)
    async def whoIsTheBuffest(self, ctx):
        await self.respond("Wiklem", ctx.message.author.mention)


    @commands.command(name="smugadd", pass_context=True)
    async def add_smug(self, ctx, path):
        allowed_content = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/gif': 'gif'}
        if not global_methods.is_admin(ctx.message.author):
            await self.bot.say("You're not a big boy")

        async with aiohttp.get(path) as r:
            if r.status == 200:
                file = await r.content.read()
                type = r.headers['Content-Type']
        if type not in allowed_content:
            await self.bot.say("That kind of file is not allowed")
            return
        else:
            hash = hashlib.md5(file).hexdigest()
            filename = "smug-anime-faces/{}.{}".format(hash, allowed_content[type])
            with open(filename, 'wb') as f:
                f.write(file)
            await self.bot.say("Smugness levels increased")


    @commands.command(name="smug", pass_context=True)
    async def smug(self, ctx):
        path = 'smug-anime-faces' # The folder in which smug anime face images are contained
        face = os.path.join(path, random.choice(os.listdir(path))) # Generate path to a random face
        # Send the image to the channel where the smug command was triggered
        await self.bot.send_file(ctx.message.channel, face)

    async def respond(self, msg, author):
        await self.bot.say("{}, {}".format(msg, author))


def get_random_line(file):
    with open(file, 'r') as f:
        line = next(f)
        for num, a in enumerate(f):
            if random.randrange(num + 2): continue
            line = a
    return line.rstrip()


def setup(bot):
    bot.add_cog(Command(bot))


if __name__ == "__main__":
    print("hello main!")


