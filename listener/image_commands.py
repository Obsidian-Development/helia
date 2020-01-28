import discord
from discord.ext import commands
from .core.image import Reddit, Subreddits, Gag, Sections

subreddits = Subreddits()
sections = Sections()

class ImageListener(commands.Cog):
    """Image listener cogs"""

    def __init__(self, client):
        self.client = client
        self.reddit = Reddit()
        self.gag    = Gag()

    def get_embedded_gag(self, section):
        """Get 9gag post from given section.
        Sections : Anime & manga, Kpop, wtf, savage, comic.
        """

        post = self.gag.get_post_from(section)
        embed = discord.Embed(color = discord.Colour(value=11735575).orange())
        embed.set_image(url=post.get_media_url())
        return embed

    async def get_embedded_submission(self, subreddit):
        """Get reddit submission from given subreddit title."""

        submission = await self.client.loop.run_in_executor(None, lambda: self.reddit.get_submission(subreddit))
        embed = discord.Embed(color = discord.Colour(value=11735575).orange())
        embed.set_image(url=submission.url)
        return embed

    async def get_embedded_search_post(self, keywords):
        """Search & get submission from subreddit"""

        submission = await self.client.loop.run_in_executor(None, lambda: self.reddit.search_get_post(keywords))
        embed = discord.Embed(color = discord.Colour(value=11735575).orange())
        embed.set_image(url=submission.url)
        return embed

    @commands.command(name='kpop', aliases=['KPOP'])
    async def kpop_(self, ctx):
        await ctx.send(embed=self.get_embedded_gag(sections.KPOP))

    @commands.command(name='anime9', aliases=['ANIME9'])
    async def anime_nine(self, ctx):
        await ctx.send(embed=self.get_embedded_gag(sections.ANIME_MANGA))

    @commands.command(name='wtf', aliases=['WTF'])
    async def wtf_nine(self, ctx):
        await ctx.send(embed=self.get_embedded_gag(sections.WTF))

    @commands.command(name='savage', aliases=['SAVAGE'])
    async def savage_nine(self, ctx):
        await ctx.send(embed=self.get_embedded_gag(sections.SAVAGE))

    @commands.command(name='comic', aliases=['COMIC'])
    async def comic_nine(self, ctx):
        await ctx.send(embed=self.get_embedded_gag(sections.COMIC))

    @commands.command()
    async def meme(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.MEMES)
            )

    @commands.command()
    async def rwtf(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.WTF)
            )

    @commands.command()
    async def dank(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.DANKMEMES)
            )

    @commands.command()
    async def aniwallp(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.ANIMEWALLPAPER)
            )

    @commands.command()
    async def animeme(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.ANIMEMES)
            )

    @commands.command()
    async def waifu(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.WAIFU)
            )

    @commands.command()
    async def fgo(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.GRANDORDER)
            )

    @commands.command()
    async def fgoart(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.FGOFANART)
            )

    @commands.command()
    async def tsun(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.TSUNDERES)
            )

    @commands.command()
    async def anime(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.ANIME)
            )

    @commands.command()
    async def scathach(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.SCATHACH)
            )

    @commands.command()
    async def moescape(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.MOESCAPE)
            )
    
    @commands.command()
    async def saber(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.SABER)
            )

    @commands.command()
    async def raikou(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_submission(subreddits.MAMARAIKOU)
            )
            
    @commands.command()
    async def abby(self, ctx):
        await ctx.send(
            embed=await self.get_embedded_search_post("fate abby")
            )
    
    @commands.command(aliases=['r/', 'reddit_search', 'reddit'])
    async def search_get_reddit(self, ctx, *keywords):
        await ctx.send(
            embed=await self.get_embedded_search_post(" ".join(keywords))
            )

def setup(client):
    client.add_cog(ImageListener(client))
    print('ImageListener is Loaded')
