import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord_components import Button, ButtonStyle, DiscordComponents

# from discord_slash import cog_ext
from scripts.calculator import buttons, calculate


class Calculator(commands.Cog, name="Calculator"):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Calculator"
        self.dc = DiscordComponents(self.bot)

    @commands.guild_only()
    @commands.command(description="Calculator command")
    async def calculator(self, ctx):
        m = await ctx.send(content="Loading Calculators...")
        expression = "None"
        delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        e = discord.Embed(
            title=f"{ctx.author.name}'s calculator",
            description=f"```xl\n{expression}```",
            timestamp=delta,
            color=discord.Colour.blurple(),
        )
        await m.edit(content="", components=buttons, embed=e)
        done = [[
            Button(style=ButtonStyle.grey, label="·", disabled=True),
        ]]
        while m.created_at < delta:
            res = await self.bot.wait_for("button_click")
            if (res.author.id == ctx.author.id
                    and res.message.embeds[0].timestamp < delta):
                expression = res.message.embeds[0].description[6:-3]
                if expression == "None" or expression == "An error occurred.":
                    expression = ""
                if res.component.label == "Exit":
                    await res.respond(
                        type=7,
                        embed=discord.Embed(
                            title="Closing down",
                            description="Calculator was terminated",
                            color=0xDD2E44,
                        ),
                        components=done,
                    )
                    break
                elif res.component.label == "←":
                    expression = expression[:-1]
                elif res.component.label == "Clear":
                    expression = "None"
                elif res.component.label == "=":
                    expression = calculate(expression)
                # elif res.component.label == "x²":
                # expression += "²"
                # elif res.component.label == "x³":
                # expression += "³"
                elif (len(expression) > 9 or expression.count("²") >= 4
                      or expression.count("³") >= 4
                      or expression.count("²²") > 1
                      or expression.count("³³") > 1
                      or expression.count("²²³³") >= 1):
                    allowed = [
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "00",
                        "0",
                        ".",
                        "(",
                        ")",
                        "π",
                        "x²",
                        "x³",
                    ]
                    if res.component.label in allowed:
                        await m.edit(
                            content="Preparing to tear down the buttons")

                        await res.respond(
                            type=7,
                            embed=discord.Embed(
                                title="Closing down",
                                description="You have entered a number that is 9 or more in length or some enormous calculation - for the stability of the bot and crash prevention we will close down this calculator session",
                                color=0xDD2E44,
                            ),
                            components=done,
                        )
                        break
                    elif (expression.count("²") == 4
                          or expression.count("³") == 4
                          or expression.count("²²") > 1
                          or expression.count("³³") > 1
                          or expression.count("²²³³") >= 1):
                        await m.edit(
                            content="Preparing to tear down the buttons")

                        await res.respond(
                            type=7,
                            embed=discord.Embed(
                                title="Closing down",
                                description="You have entered a number that is 9 or more in length or some enormous calculation - for the stability of the bot and crash prevention we will close down this calculator session",
                                color=0xDD2E44,
                            ),
                            components=done,
                        )
                        break
                    else:
                        await m.edit(
                            content="Preparing to tear down the buttons")

                        await res.respond(
                            type=7,
                            embed=discord.Embed(
                                title="Closing down",
                                description="You have entered a number that is 9 or more in length or some enormous calculation - for the stability of the bot and crash prevention we will close down this calculator session",
                                color=0xDD2E44,
                            ),
                            components=done,
                        )
                        break
                else:
                    expression += res.component.label
                f = discord.Embed(
                    title=f"{ctx.author.name}'s calculator",
                    description=f"```xl\n{expression}```",
                    timestamp=delta,
                    color=discord.Colour.blurple(),
                )
                await res.respond(content="",
                                  embed=f,
                                  components=buttons,
                                  type=7)


def setup(bot):
    bot.add_cog(Calculator(bot))
