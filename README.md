<p align="center">
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
<img align="center" src="https://raw.githubusercontent.com/pieckenst/helia/current/heliacircle.png" height="140" width="140">
</p>

<p align="center">
<img align="center" src="https://raw.githubusercontent.com/pieckenst/helia/current/bitmapm.png" height="100" width="320">
</p>

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![GitHub last commit](https://img.shields.io/github/last-commit/pieckenst/helia?style=for-the-badge)](https://github.com/pieckenst/helia/commits/current)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/pieckenst/helia/canary?color=ff4500&label=CANARY%3ALAST%20COMMIT&style=for-the-badge)](https://github.com/pieckenst/helia/commits/canary)
[![GitHub](https://img.shields.io/github/license/pieckenst/helia?style=for-the-badge)](https://github.com/pieckenst/helia/blob/master/LICENSE)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

<div align="center">
<h3 align="center">An opensource music and moderation bot made for your pleasure)</h3>  
<h3 align="center">Main bot features</h3>
<h3 align="center"> Music </h3>
<h3 align="center"> Moderation </h3>
<h3 align="center"> Information Commands and wikipedia Search</h3>
</div>

Moderation features ( like ban, kick , clear mute , and unmute ) You can also view user information and profile picture

Wiki commands as well as wikipedia search You can use //wiki to search on wikipedia As well as the bot includes some commands to see short bits of info on a few of linux distributions

More info on bot features can be seen in //help and you can always contribute to betterment of the bot if you know python by heading to the bot repository on github at https://github.com/pieckenst/helia and following our contributing guidelines at https://github.com/pieckenst/helia/blob/master/CONTRIBUTING
Source code on public github can be a bit behind hosted version since updates to it are pushed when enough changes pile up

Russian Description

Бот с открытым исходным кодом для модерации и музыки Основные возможности бота Музыка (может иногда ломаться) Бот может воспроизводить музыку с YouTube, пропускать ее, есть очередь, обычные вещи для музыкальных ботов в целом

Функции модерации (например, ban,kick,mute,unmute).  Имеется возможность просматривать информацию о пользователе и смотреть аватарку профиля.

Информационные команды а также поиск в википедии. Вы можете использовать //wiki для поиска в википедии. Кроме того, бот включает несколько команд для просмотра короткой информации о некоторых дистрибутивах Linux.

Более подробную информацию о функциях бота можно увидеть в //help, и вы всегда можете внести свой вклад в улучшение бота, если знаете python, перейдя в репозиторий бота на github по адресу https://github.com/pieckenst/helia и сделать изменения сответствуя нашим требованиям для пул реквестов на https://github.com/pieckenst/helia/blob/master/CONTRIBUTING. Исходный код на общедоступном github может немного отставать от захосченной версии, поскольку обновления в него отправляются, когда накапливается достаточно изменений

# BOT HOSTING GUIDE
1. Create .env file in src folder with this content
DISCORD_TOKEN=your token without quote symbols or anything
2. If you want to host localy then just launch the bot with py main.py otherwise follow next steps
3. Heroku cli setup
4. Follow step 1 
5. Go to heroku.com and Sign Up or Log In if already have an account.
6. For command line setup install Git and do git init when inside your directory
7. Install heroku cli
8. Then do heroku apps:create name_of_app and heroku buildpacks:set heroku/python
9. Finally, do git push heroku master or git push heroku branch_name:master if you want to only push one branch
10. For heroku gui setup do
11. Go to heroku.com and Sign Up or Log In if already have an account.
12. Go to Heroku Dashboard
13. Hit New. Now give the application on heroku a unique name
14. Click on Connect to Github. You might need to Authorize the app. If so Do It. 
15. Create a private repository on github 
16. Upload bot files into your private repository and edit gitignore and remove .env file mentions from there
17. Create .env file in src folder of your private repository with this content
DISCORD_TOKEN=your token without quote symbols or anything
18. Now go back to heroku and link your private repository there by entering your name of private repository. Hit search and then connect.
19. Now scroll down below and Enable Auto Deploy. Now Scroll a little more and hit Deploy Branch.
# Enabling the bot to launch in heroku
20. Go to Resources Tab once the bot deployement is finished
21. Click the little edit icon near our apps' name to enable our dynos
22. Enable it and hit confirm
23. Congrats you now have your own helia instance

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Sviat946"><img src="https://avatars.githubusercontent.com/u/83779551?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sviat946</b></sub></a><br /><a href="#ideas-Sviat946" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://discord.gg/5JEb7ju"><img src="https://avatars.githubusercontent.com/u/52179357?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nigaman</b></sub></a><br /><a href="https://github.com/Helia-Developers/helia/commits?author=NigamanRPG" title="Code">💻</a></td>
    <td align="center"><a href="http://arslee.tk"><img src="https://avatars.githubusercontent.com/u/50916030?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Arsenii Liunsha</b></sub></a><br /><a href="https://github.com/Helia-Developers/helia/commits?author=arslee07" title="Code">💻</a> <a href="#translation-arslee07" title="Translation">🌍</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!