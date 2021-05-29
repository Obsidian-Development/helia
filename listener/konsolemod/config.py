import discord
import asyncio
import sqlite3
import random
from scripts import db
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import os
class config(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    #@commands.command()
    #async def prefix(self,ctx,*, prefix_n=None):
        #try:
            #author = ctx.message.author
            #if author.guild_permissions.administrator:
                #if prefix_n is None:
                    #return await ctx.send("bot: Write the prefix")
                #connect = sqlite3.connect(db.main)
                #cursor = connect.cursor()
                #cursor.execute(db.select_table("prefixes", "prefix", "guild_id", ctx.guild.id))     
                #result = cursor.fetchone()
                #if result is None:
                    #val = (ctx.guild.id, prefix_n)
                    #cursor.execute(db.insert_table("prefixes","guild_id","prefix"), val)
                #else:
                    #val = (prefix_n, ctx.guild.id)
                    #cursor.execute(f"UPDATE prefixes SET prefix = ? WHERE guild_id = ?", val)  
                #connect.commit()
                #cursor.close()
                #connect.close()
                #await ctx.send(f"bot: Changed the prefix to ``{prefix_n}``")
            #else:
                #await ctx.send("bot: You do not have enough permissions - :You require **Administrator**.")
        #except:
            #await ctx.send("bot: Error , wrong argument or not enough permissions")

    @commands.group(invoke_without_command=True)
    async def verify(self, ctx: SlashContext):
        try:
            conn = sqlite3.connect(db.main)
            cursor = conn.cursor()
            cursor.execute(db.select_table("verify", "role_id", "guild_id", ctx.guild.id))
            res = cursor.fetchone()
            if res is None:
                return await ctx.send("bot: Verification role not set , contact the administrator.")
            role = discord.utils.get(ctx.guild.roles, id=int(res[0]))
            if role in ctx.author.roles:
                return await ctx.send("bot: You already have this role")
            passcode=""
            indent=5
            rng = random.randint(4,6)
            length = 30 * rng
            fnt = ImageFont.truetype('captcha/govnofont.ttf', 68)
            img = Image.new('RGB', (length, 70), color = (255, 255, 255))
            d = ImageDraw.Draw(img)
            for u in range(rng):
                u = str(random.randint(0, 9))
                d.text((indent, random.randint(0, 10)), u, font=fnt, fill=(0, 0, 0))
                passcode += u
                indent += 26
            path = f'captcha/captcha-{ctx.message.author.id}.png'
            img.save(path)
            await ctx.send(file=discord.File(path))
            msg = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=50.0)
            if int(msg.content) == int(passcode):
                await ctx.message.author.add_roles(role)
                await ctx.send("bot: The verification is done , role granted.")
            else:
                await ctx.send("bot: Error , captcha not done")
        except:
            await ctx.send("bot: Error.")



    @verify.command()
    async def role(self, ctx: SlashContext, ver_role: discord.Role=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.administrator:
                conn = sqlite3.connect(db.main)
                cursor = conn.cursor()
                cursor.execute(db.select_table("verify", "role_id", "guild_id", ctx.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.guild.id, ver_role.id)
                    cursor.execute(db.insert_table("verify", "guild_id", "role_id"), val)
                else:
                    cursor.execute(db.update_table("verify", "role_id", ver_role.id, "guild_id", ctx.guild.id))
                conn.commit()
                cursor.close()
                conn.close()
                await ctx.send(f"bot: Set the verification role to ``{ver_role.name}``")
            else:
                await ctx.send("bot: You do not have enough permissions - :You require **Administrator**.")
        except:
            await ctx.send("bot: Error , wrong argument or not enough permissions")
        

    @verify.command(pass_context=True)
    async def clear(self, ctx: SlashContext):
        try:
            author = ctx.message.author
            if author.guild_permissions.administrator:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(db.select_table("verify", "role_id", "guild_id", ctx.guild.id))
                result = cursor.fetchone()
                if result is None:
                    await ctx.send("bot: Do not have a table for the goodbye channel - Check Database.")
                else:
                    cursor.execute(db.delete_table("verify", "guild_id", ctx.guild.id))
                    await ctx.send("bot: Cleared the table")  
                connect.commit()
                cursor.close()
                connect.close()        
            else:
                await ctx.send("bot: You do not have enough permissions - :You require **Administrator**.")
        except:
            await ctx.send("bot: Error")
    

def setup(bot):
    bot.add_cog(config(bot))
