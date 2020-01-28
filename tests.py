from listener.core.image import Subreddits, Reddit

if __name__ == "__main__":
    reddit_client = Reddit()
    submissions = list(reddit_client.reddit.subreddit('all').search('fate raikou',params={'include_over_18': 'on'}))
    for submission in submissions:
        print(submission.title, "\n", submission.url, "\n", submission.over_18)
