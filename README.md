<p align="center">
    <a href="https://github.com/hearot/pyroboard">
        <img src="https://i.imgur.com/XhInvbp.gif" alt="Pyroboard" width="150"/>
    </a>
    <br>
    <b>A simple and intuitive menu handler for Pyrogram</b>
    <i>Create your own in less than 100 lines!</i>
    <br>
    <br>
    <a href="https://github.com/hearot/pyroboard/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/License-GPL%20v3-red.svg" alt="License: GPLv3"/>
    </a>
    <a href="https://t.me/hearot">
        <img src="https://img.shields.io/badge/Developer-@hearot-blue.svg" alt="Developer: @hearot"/>
    </a>
</p>

## Pyroboard

```python
from pyroboard import TreeHandler, TreeMenu, transform_dict
from pyrogram import Client

bot = Client("sample_bot", api_hash=input("API hash: "),
             api_id=input("API ID: "),
             bot_token=input("Bot token: "))

handler = TreeHandler(transform_dict(
    {
        TreeMenu("Main", "main", "Hello!"): {
            TreeMenu("About me", "about_me", "I'm just a bot"): None,
            TreeMenu("Thoughts", "thoughts",
                     "I'm a bot, I cannot think properly..."): None
        }
    }
))

handler.setup(bot)
bot.run()
```

### Copyright & License

- Copyright (C) 2020 [Hearot](https://github.com/hearot)
- Licensed under the terms of the [GNU General Public License v3 (GPLv3)](LICENSE)
