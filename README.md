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
from pyrubrum import Handler, transform_dict, Menu

bot = Client(...)

handler = Handler(transform_dict(
    {
        Menu("Main", "main", "Hello!"): {
            Menu("About me", "about_me", "I'm just a bot!"),
            Menu("Thoughts", "thoughts",
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

### Commit messages

> *See [Conventional Commits](https://www.conventionalcommits.org).*

### Versioning

> *See [PEP 440](https://www.python.org/dev/peps/pep-0440/).*

### Thanks

   - [veggero/tytg](https://github.com/veggero/tytg) for giving me the idea of developing a simple framework which you can code a folder-like bot with.
   - [IlhomBahoraliev/pyromenu](https://github.com/IlhomBahoraliev/pyromenu) for letting me understand that an object-oriented library would make the difference in developing this project.

### Copyright & License

- Copyright (C) 2020 [Hearot](https://github.com/hearot)
- Licensed under the terms of the [GNU General Public License v3 (GPLv3)](./LICENSE)
