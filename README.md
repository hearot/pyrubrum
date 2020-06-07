<p align="center">
    <a href="https://github.com/hearot/pyrubrum">
        <img src="https://i.imgur.com/XhInvbp.gif" alt="Pyrubrum" width="150"/>
    </a>
    <br>
    <b>An intuitive framework for creating Telegram bots.</b>
    <br>
    <i>Create your own bot in less than 100 lines!</i>
    <br>
    <br>
    <a href="https://github.com/hearot/pyrubrum/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/License-GPL%20v3-red.svg" alt="License: GPLv3"/>
    </a>
    •
    <a href="https://t.me/hearot">
        <img src="https://img.shields.io/badge/Developer-@hearot-blue.svg" alt="Developer: @hearot"/>
    </a>
</p>

## Pyrubrum

```python
from pyrogram import Client
from pyrubrum import transform_dict, TreeHandler, TreeMenu

bot = Client(...)

handler = TreeHandler(transform_dict(
    {
        TreeMenu("Main", "main", "Hello!"): {
            TreeMenu("About me", "about_me", "I'm just a bot!"),
            TreeMenu("Thoughts", "thoughts",
                     "I'm a bot, I cannot think properly...")
        }
    }
))

handler.setup(bot)
bot.run()
```

**Pyrubrum** is a versatile, charming framework for creating [Telegram](https://telegram.org) [bots](https://core.telegram.org/bots), jointly with [Pyrogram](https://github.com/pyrogram/pyrogram).

### Examples

In order to make use of the proposed examples, you need to create your own environment file by renaming [sample.env](./examples/sample.env) into `.env` and editing all the necessary variables.

   - [Calendar](./examples/calendar_bot.py) - Get what day of the week a day is by simply choosing a year, a month and a day while discovering the potential of Pyrubrum page menus.
   - [Sample](./examples/sample_bot.py) - Interact with inline menus while understanding how Pyrubrum works.

### Copyright & License

- Copyright (C) 2020 [Hearot](https://github.com/hearot)
- Licensed under the terms of the [GNU General Public License v3 (GPLv3)](./LICENSE)
