# R3NAUT

[![Contributors][contributors-shield]][contributors-url]
[![Last commit][last-commit-shield]][last-commit-url]
[![Issues][issues-shield]][issues-url]
[![BSD 3-Clause License][license-shield]][license-url]
[![Stargazers][stars-shield]][stars-url]

<p align="center">
  <a href="https://github.com/Guard-SK/R3NAUT">
    <img src="README-images/R3NAUT.png" alt="R3NAUT profile picture" width="200" height="200">
  </a>

  <h3 align="center">An awesome Discord moderatiob bot!</h3>

  <p align="center">
    Single server moderation/fun bot
    <br />
    <a href="https://discord.gg/3u8aMBzNBJ"><strong>Join the server the bot is in »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Guard-SK/R3NAUT/issues">Report Bug</a>
    ·
    <a href="https://github.com/Guard-SK/R3NAUT/issues">Request Feature</a>
  </p>
</p>

## Hello!
Hi! My name is Guard, and this is my bot. I built it, because I wanted to learn python and the best (and fun) way that showed up to me was discord.py. 

### About the past of the bot
This bot is built by tutorial from Carberra (link at the end of README), but edited to function on my server. I'm trying to get away from Carberra's tutorials, so some of the features are different, but the base of the code is the same as Carberra. Really recommend checking him out if you want to start with discorrd.py or learn more about discord moderation bot coding.

## What does he bring today?
So... there is a lot to talk about ngl. This project gotten pretty big and has some goooood features I'm proud of. So we shall start with:

### Public commands
Although this bot is designed to be moderation, there is something to talk about in the public section of the bot. Here is the list of the public commands with description:

#### Prefix = 3
#### 3help

| Name\|Aliases  | Command description |
| ------------- | ------------- |
| hi\|hello\|sup  | greetings  |
| fact (animal)  | fact about dog, cat, panda, fox, bord or koala  |
| dice\|roll (number of dices)d(highest number on the dice)  | rolls dices of your choice  |
| say\|echo (content)  | repeat content of your message  |
| slap\|hit (member) (reason)  | slaps someone for some reason  |
| dm\|direct message\|send (member) (content)  | sends a dm to someone  |
| serverinfo\|si\|guildinfo\|gi | info about the server |
| userinfo|ui (member)  | gives you info about the user you mentioned  |
| ping  | pong  |
| botinfo  | info about R3NAUT  |

### Admin/moderation commands
So as we said, this is a moderation bot, and moderation bots are for moderation. So this bot has something called admin commands. Here is the list of the commands:

#### 3ahelp

| Name\|Aliases  | Command description |
| ------------- | ------------- |
| addprofanity\|addswears\|addcurses (words) | add forbidden words. *Permissions: Admin and higher* |
| delprofanity\|delswears\|delcurses (words) | delete forbidden words. *Permissions: Admin and higher* |
| mute (member) (time in minutes(optional)) | deletes all roles from mentioned user and adds a mute role. If you typed time as well, bot will delete the roles and add the old once back. *Permissions: Moderator and higher* |
| unmute (member) | deletes muted role and adds old roles back. *Permissions: Moderator and higher* |
| clear|purge|nuke (number) (member(s)(optional)) | clears number of messages you typed. If you mentioned user, the bot will clear all messages within the number you typed that are written by user(s) you mentioned. *Permissions: Moderator and higher* |
| kick (member) (reason) | kick user you mentioned. *Permission: Moderator and above* |
| ban (member) (reason) | bans member you mentioned. *Permission: Staff and higher* |

### Other moderation features
We are done with commands, but there is some other features that the bot can do. First of we can start with
#### Logging
This is a great feature that helps A-team to catch up and be alerted about what happened on the server. Here you have a image, so you can have idea how does it looks like:

<p align="center">
  <a href="https://github.com/Guard-SK/R3NAUT">
    <img src="README-images/R3NAUT.png" alt="R3NAUT profile picture">
  </a>
</p>

*If you want to see full code, go to lib/cogs/log.py*
#### And last Auto-moderation
Yeah there is a auto-moderation feature in this bot. This feature is not completed, but the first basic things are public. This bot can detect if you'r spamming mentions, and mute you for 5 minutes if that's the case.

### Languages and hosting

#### Python
The bot is fully made in discord.py

#### SQL database
The bot's database is made in SQL

#### Hosting
The bot is hosted on https://hostsapling.net/

### Links
<p>
Carberra - https://www.youtube.com/channel/UC13cYu7lec-oOcqQf5L-brg
</p>
<p>
Carberra moderation tutorial - https://www.youtube.com/watch?v=F1HbEOp-jdg&list=PLYeOw6sTSy6ZGyygcbta7GcpI8a5-Cooc&ab_channel=CarberraTutorials
</p>
<p>
README template - https://github.com/othneildrew/Best-README-Template
</p>
<p>
My discord server - https://discord.gg/3u8aMBzNBJ
</p>

<!-- SHIELD LINKS & IMAGES -->
[issues-shield]: https://img.shields.io/github/issues/Guard-SK/R3NAUT
[issues-url]: https://github.com/Guard-SK/R3NAUT/issues
[license-shield]: https://img.shields.io/github/license/Guard-SK/R3NAUT
[license-url]: https://github.com/Guard-SK/R3NAUT/blob/main/LICENSE.txt
[last-commit-shield]: https://img.shields.io/github/last-commit/Guard-SK/R3NAUT
[last-commit-url]: https://github.com/Guard-SK/R3NAUT/graphs/commit-activity
[stars-shield]: https://img.shields.io/github/stars/Guard-SK/R3NAUT?style=social
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[contributors-shield]: https://img.shields.io/github/contributors/Guard-SK/R3NAUT
[contributors-url]: https://github.com/Guard-SK/R3NAUT/graphs/contributors