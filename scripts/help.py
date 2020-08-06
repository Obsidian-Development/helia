categories = """
```Help System.```
Prefix: ``{}``
More Information: ``help [Module]``

-----------------------------------
**moderation** - Moderation module
**minigames** - Minigames module
**fun** - Fun Module
**music** - Music Module
**infosystem** - Information module
**system** - Submission and ticket creation information 
**config** - Settings for server setup 
**tools** - Useful tools
**sudo** - Help for bot owners

**Use $invite for bot invite links**
""" 

mod = """
```Help. Module: Moderation```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``ban [User] {Reason}`` - User Ban
``kick [User] {Reason}`` - Kick user
``rmmod [User] {Reason}`` - Mute User
``unrmmod [User]`` - Unmute User
``clear [Amount]`` - Clear messages
``clear user [User] [Amount]`` - Clear messages from mentioned user
"""

minigames = """
```Help. Module: Minigames```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``kubik`` - Roll the dice (Results: a number from 1 to 6)
``monetka`` - Coin Toss (2 results)
``casino`` - Play Casino
"""

fun = """
```Help. Module: Fun```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``echo [text]`` - Send a message from bot name
"""

music = """
```Help. Module: Music```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``play [url]`` - Play Music/Video From youtube
``pause`` - Pauses playback of track
``resume`` - Resumes playback of track
``np`` - Shows info about current track
``stop`` - Stops playback
``skip`` - Skips current track
``queue`` - Music queue
``volume`` - Change volume
"""

infosystem = """
```Help. Module: InfoSystem```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``neofetch {User}`` - Information about user
``avatar {User}`` - User profile picture
``guild`` - Information about server
``voicedemo [VoiceChannel]`` - Get a link for screenshare in voice channel"""

config = """
```Help. Module: Configuration```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``welcome channel [TextChannel] | clear`` - Sets a channel for welcome messages | Clears configuration in database
``goodbye channel [TextChannel] | clear`` - Sets a channel for farewell messages | Clears configuration in database
``sub channel [TextChannel] | clear`` - Sets a channel for suggestion messages | Clears configuration in database
``ticket channel [TextChannel] | clear`` - Sets a channel for ticket messages | Clears configuration in database
``prefix [Prefix]`` - Set the prefix for this guild
``verify role | clear`` - Set the verification role | clear the verification role
TEXT: {MEMBER} = User tag; {MENTION} = Mention of  the user
"""

tools = """
```Help. Module: Tools```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``embed [Title] [Content]`` - Creates a embed with your text
``remind me | role [Time] [Message]`` - Creates a reminder for you | for role
``arch`` information about a linux distribution named Arch linux
``debian`` information about a linux distribution named Debian
``ubuntu`` information about a linux distribution named Ubuntu
``deepin`` information about a linux distribution named Deepin
``mint``  information about a linux distribution named Linux Mint
``manjaro`` information about a linux distribution named Manjaro
``wallpaper`` get some nice wallpapers
``wiki`` search for something on wikipedia
"""

system = """
```Help. Module: System```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``sub create [Text]`` - Create a suggestion
``ticket create [Text]`` - Send a ticket to administration"""

sudo = """
```Help. Module: Owner configuration```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``shutdown`` - Bot Shutdown
``set_status`` - Set bot status"""


# HELP для команд
goodbye = """
```Help. Command: Goodbye```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``goodbye channel [TextChannel]`` - Set a farewell channel
``goodbye clear`` - clear database info
``goodbye text`` - set the text for a farewell
""" 

welcome = """
```Help. Command: Welcome```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``welcome channel [TextChannel]`` - Set a welcome channel
``welcome clear`` - clear database info
``welcome text`` - set the text for a welcome
""" 

submit = """
```Help. Command: Sub```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``sub channel [TextChannel]`` - set a channel for suggestions/votes
``sub clear`` - clear database info
``sub create [Content]`` - create vote/suggestion"""

tickets = """
```Help. Command: Ticket```
[ARG] - Required Argument | {ARG} - Optional Argument
-----------------------------------
``ticket channel [TextChannel]`` - set a channel for tickets
``ticket clear`` - clear database info
``ticket create [Content]`` - create ticket"""
###




