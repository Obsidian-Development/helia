import aiohttp
import requests
import asyncio
import pprint as pp

_TIMEOUT  = 30

_BASE_URL = 'https://api.github.com'

_METHOD_MAP = dict(
    GET='GET',
    POST='POST'
)

class GithubRepository:
    """Represents 'Github's repository data."""

    def __init__(self):
        self.id = 0
        self.full_name = ''
        self.name = ''
        self.open_issues = 0
        self.open_issues_count = 0
        self.download_url = ''
        self.html_url = ''
        self.watchers = 0
        self.watchers_count = 0
        self.updated_at = ''
        self.pushed_at = ''
        self.created_at = ''
        self.forks = 0
        self.forks_count = 0
        self.description = ''
        self.clone_url = ''
        self.default_branch = 'master'
        self.git_url = ''
        self.language = ''
        self.languages = ''
        self.license = None
        self.owner = None

    def process_raw(self, repo_raw):
        """Set all attributes with the given repo_raw (json types)."""

        self.id = repo_raw['id']
        self.name = repo_raw['name']
        self.full_name = repo_raw['full_name']
        self.pushed_at = repo_raw['pushed_at']
        self.created_at = repo_raw['created_at']
        self.updated_at = repo_raw['updated_at']
        self.clone_url = repo_raw['clone_url']
        self.description = repo_raw['description']
        self.language = repo_raw['language']
        self.license = repo_raw['license']
        self.html_url = repo_raw['html_url']

class GithubOwner:
    """Represents 'Github's owner data."""

    def __init__(self):
        self.avatar_url = ''
        self.followers_url = ''
        self.following_url = ''
        self.starred_url = ''
        self.url = ''
        self.html_url = ''
        self.raw = None

class AioGithub:
    """Asynchronous Github Client"""

    def __init__(self, loop=None):
        self.loop = loop

    async def search_user(self, q):
        """Search user by keyword"""

        async with aiohttp.ClientSession() as session:
            url = "{}/search/users?q={}".format(_BASE_URL, q)
            async with session.get(url) as response:
                return await response.json()

    async def get_user(self, username):
        """Get user data from given username."""

        async with aiohttp.ClientSession() as session:
            url = "{}/users/{}".format(_BASE_URL, username)
            async with session.get(url) as response:
                return await response.json()

    async def search(self, category="repositories", q=""):
        """Search by category & keyword.

        More flexible way to search.
        params:
        category -> repositories, topics, code, commits, issues, users
        q        -> keyword
        """

        async with aiohttp.ClientSession() as session:
            url = "{}/search/{}?q={}".format(_BASE_URL, category, q)
            async with session.get(url) as response:
                return await response.json()

    async def get_user_repos(self, username, raw=True, max_response=10):
        """Get user's repositories."""

        async with aiohttp.ClientSession() as session:
            url = "{}/users/{}/repos".format(_BASE_URL, username)
            async with session.get(url) as response:
                if raw:
                    return await response.json()
                else:
                    repos_raw = await response.json()
                    repos = []
                    for i, repo_raw in enumerate(repos_raw):
                        repo = GithubRepository()
                        repo.process_raw(repo_raw)
                        repo.languages = await self.get_user_repo_languages(
                            username=username, repo=repo.name
                        )
                        repo.owner = await self.get_user(username=username)
                        repos.append(repo)
                        if i == max_response - 1:
                            break
                    return repos

    async def get_user_repo_languages(self, username, repo):
        """Get repostory's languages from given username and repo's name."""

        async with aiohttp.ClientSession() as session:
            url = "{}/repos/{}/{}/languages".format(_BASE_URL, username, repo)
            async with session.get(url) as response:
                return await response.json()

class Github:
    def __init__(self, loop=None):
        self._memo = {}
        self.loop = loop

    async def search(self, category="repositories", q=''):
        url = "{}/search/{}?q={}".format(_BASE_URL, category, q)
        response = await self.loop.run_in_executor(None, lambda: requests.get(url))
        return response.json()

# TESTS
if __name__ == '__main__':
    async def main():
        aiog = AioGithub()
        repos = await aiog.get_user_repos('MadeYoga', raw=False)
        for repo in repos:
            print(repo.full_name)
            print(repo.owner)
            print(repo.languages)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
