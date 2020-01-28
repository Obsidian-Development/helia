from .nineapi.nineapi.client import  Client, APIException
import os
import random
import praw
from . import config

class Sections:
    ANIME_MANGA = 32
    WTF         = 4
    SAVAGE      = 45
    KPOP        = 34
    COMIC       = 17

class Gag:
    def __init__(self):
        self.gag_client = Client()
        self.gag_client.log_in(
            config.GAG_USERNAME,
            config.GAG_PASSWORD
            )

    def get_post_from(self, group_id):
        try:
            post = random.choice(
                self.gag_client.get_posts(
                    group=group_id,
                    count=50,
                    type_='hot',
                    entry_types=['photo', 'animated']
                )
            )
        except:
            # reconnect
            self.gag_client.log_in(
                config.GAG_USERNAME,
                config.GAG_PASSWORD
                )
            post = random.choice(
                self.gag_client.get_posts(
                    group=group_id,
                    count=50,
                    type_='hot',
                    entry_types=['photo', 'animated']
                )
            )
        return post

class Subreddits:
    MEMES           = "memes"
    DANKMEMES       = "dankmemes"
    WTF             = "wtf"
    GRANDORDER      = "grandorder"
    WAIFU           = "Waifu"
    SCATHACH        = "scathach"
    FGOFANART       = "FGOfanart"
    ANIME           = "anime"
    ANIMEMES        = "Animemes"
    AWWNIME         = "awwnime"
    AZURELANE       = "AzureLane"
    TSUNDERES       = "Tsunderes"
    ANIMEWALLPAPER  = "Animewallpaper"  # ANIME WALLPAPER ARTS
    MOESCAPE        = "Moescape"        # ANIME WALLPAPER ARTS
    MAMARAIKOU      = "MamaRaikou"
    SABER           = "Saber"
    FGOCOMICS       = "FGOcomics"
    FATEPRISMAILLYA = "FatePrismaIllya"
    ILLYASVIEL      = "Illyasviel"

class Reddit:
    def __init__(self):
        self.reddit = praw.Reddit (
            client_id     = config.REDDIT_CLIENT_ID,
            client_secret = config.REDDIT_CLIENT_SECRET,
            user_agent    = config.REDDIT_USER_AGENT
        )

    def get_submission(self, subreddit):
        submissions = list(self.reddit.subreddit(subreddit).hot())
        while True:
            submission = random.choice(submissions)
            if not submission.stickied and '.' in str(submission.url)[-5:]:
                break
        return submission

    def search_post(self, keyword):
        return self.reddit.subreddit('all').search(keyword)
        
    def search_get_post(self, keyword):
        submissions = list(self.reddit.subreddit('all').search(keyword))
        while True:
            submission = random.choice(submissions)
            if not submission.stickied and '.' in str(submission.url)[-5:]:
                break
        return submission
