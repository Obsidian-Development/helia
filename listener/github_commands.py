import discord
from discord.ext import commands

from .core.github import AioGithub

class GithubListener:
    """Github commands listener cogs"""

    def __init__(self, client):
        self.client = client
        self.git_client = AioGithub()

    @commands.command(name='git -r', aliases=['repos', 'repo'])
    def _git_user_repos(self, ctx, *args):
        username = ''.join([word for word in args])
        repos = await self.git_client.get_user_repos(username=username)
        
        return

def setup(bot):
    bot.load_extension(GithubListener(bot))
    print("GithubListener is loaded")
