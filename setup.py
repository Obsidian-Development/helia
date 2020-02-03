# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['db']

package_data = \
{'': ['*'], 'db': ['goodbye/*', 'submits/*', 'tickets/*', 'welcome/*']}

install_requires = \
['aiohttp',
 'asyncio',
 'discord.py[voice]==1.2.5',
 'google-api-python-client',
 'google-auth',
 'google-auth-httplib2',
 'oauth2client',
 'praw',
 'pynacl',
 'random2',
 'simpleeval>=0.9.10,<0.10.0',
 'youtube-dl']

setup_kwargs = {
    'name': 'db',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
