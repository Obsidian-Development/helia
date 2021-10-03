import discord
from discord.ext import commands
from discord import SelectOption,ButtonStyle
from discord.ui import View, Select,Button

class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options=[
                    SelectOption(label="General", value="General"),
                    SelectOption(label="Moderation", value="Moderation"),
                    SelectOption(label="Utilities", value="Utilities"),
                    SelectOption(label="Music", value="Music"),
                    SelectOption(label="Preferences", value="Preferences"),
                    SelectOption(
                        label="Welcome & Goodbye Messages",
                        value="Welcome & Goodbye Messages",
                    ),
                    SelectOption(label="Other", value="Other"),
                    SelectOption(label="Close", value="Close"),
                ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select a category', min_values=1, max_values=1, options=options)

    #async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's 
        # selected options. We only want the first one.
        #await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(slash_interaction=True, message_command=True,description="Help Command")
    async def help(self, ctx):
        embed = discord.Embed(title="SELECTION TEST",
                              description="Testing our embeds",
                              color=0xFF8000)
        embede = discord.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
        embede.set_footer(text="Developed with ❤️ by Middlle")
        view = DropdownView()
        done_components = [
            Button(style=ButtonStyle.secondary, label="·", disabled=True),
        ]

        async def callback(interaction):
            await interaction.send(embed=embed)

        await ctx.send(embed=embede, view=view)

        while True:
            interaction = await self.bot.wait_for("select_option")
            label = interaction.values[0]
            if label == "General":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "General":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=discord.Embed(
                        title=":beginner: General",
                        description=f"Here is the list of general commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Moderation":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Moderation":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)

                await interaction.respond(
                    type=7,
                    embed=discord.Embed(
                        title=":hammer_pick: Moderation",
                        description=f"Here is the list of moderation commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Utilities":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Utilities":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=discord.Embed(
                        title=":wrench: Utilities",
                        description=f"Here is the list of utilities commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Music":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Music":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=discord.Embed(
                        title=":headphones: Music",
                        description=f"Here is the list of music commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Preferences":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Prefs":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=discord.Embed(
                        title=":tools: Preferences",
                        description=f"Here is the list of bot configuration commands \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )

            if label == "Welcome & Goodbye Messages":
                descwelcgood = """
                Here is the list of commands related to server join and leave messages
                ```welcome - Displays this message```
                .
                ```welcome channel [#channel mention] - Set welcome channel```
                .
                ```welcome clear - Remove the set welcome channel```
                .
                ```welcome text {Optionally enter text - otherwise the default will be set} - Set welcome text```
                .
                ```goodbye - Displays this message```
                .
                ```goodbye channel [#channel mention] - Set goodbye channel```
                .
                ```goodbye clear - Remove the set goodbye channel```
                .
                ```goodbye text {Optionally enter text - otherwise the default will be set} - Set goodbye text```

                """
                await interaction.respond(
                    type=7,
                    embed=discord.Embed(
                        title=":wave: Welcome & Goodbye Messages",
                        description=f"{descwelcgood}",
                    ).set_author(name="Help System"),
                )
            if label == "Other":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Other":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=discord.Embed(
                        title=":hourglass: Other",
                        description=f"Here is the list of miscellaneous commands \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Close":
                await interaction.respond(type=7,
                                          embed=embede,
                                          components=done_components)


def setup(bot):
    bot.add_cog(Help(bot))
