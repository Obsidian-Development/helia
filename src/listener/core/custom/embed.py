import discord
from discord import Embed


class CustomEmbed(Embed):
    def __init__(self):
        super().__init__(color=discord.Color(value=1).lighter_grey())
