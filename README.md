<p align="center">
    <a href="https://github.com/hearot/pyrubrum">
        <img src="https://i.imgur.com/gfkh9bR.png" alt="Pyrubrum" width="600"/>
    </a>
    <br>
    <b>An intuitive framework for creating Telegram bots.</b>
    <br>
    <i>Create your own bot in less than 100 lines!</i>
    <br>
    <br>
    <a href="https://t.me/pyrubrum">
        <img src="https://img.shields.io/badge/Channel-@pyrubrum-red.svg" alt="Channel: @pyrubrum"/>
    </a>
    •
    <a href="https://t.me/hearot">
        <img src="https://img.shields.io/badge/Developer-@hearot-blue.svg" alt="Developer: @hearot"/>
    </a>
    •
    <a href="https://github.com/hearot/pyrubrum/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/License-GPLv3-green.svg" alt="License: GPLv3"/>
    </a>
</p>

## Pyrubrum

```python
from pyrogram import Client
from pyrubrum import Handler, Menu, transform

bot = Client(...)

handler = Handler(transform(
    {
        Menu("Start", "start", "Hello!", default=True): [
            Menu("About me", "about_me", "I'm just a bot!"),
            Menu("Thoughts", "thoughts",
                 "I'm a bot, I cannot think properly..."),
        ]
    }
))

handler.setup(bot)
bot.run()
```

**Pyrubrum** ([*/ˈpaɪɹˈuːbɹəm/*](http://ipa-reader.xyz/?text=%CB%88pa%C9%AA%C9%B9%CB%88u%CB%90b%C9%B9%C9%99m&voice=Russell)) is a versatile, charming framework for creating [Telegram bots](https://core.telegram.org/bots), jointly with [Pyrogram](https://github.com/pyrogram/pyrogram).

### Features

   - Automatic [deep-link](https://core.telegram.org/bots#deep-linking) generation with `DeepLinkMenu`
   - Built-in support for [Redis](https://redis.io/)
   - [Complete documentation](https://pyrubrum.readthedocs.io/)
   - Custom styles for inline keyboards
   - Database integration
   - Fast & optimized using [MTProto](https://core.telegram.org/mtproto) jointly with [Pyrogram](https://github.com/pyrogram/pyrogram)
   - Fully encrypted parameters
   - Intuitive creation of inline keyboards
   - LRU caching with [functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)
   - Native support for the *"Go back"* button
   - No limit for `callback_data` (see [Telegram Bot API](https://core.telegram.org/bots/api#inlinekeyboardbutton))
   - Paging integration with `PageMenu`

### Examples

In order to make use of the proposed examples, you need to create your own environment file by renaming [sample.env](./examples/sample.env) into `.env` and editing all the necessary variables.

   - [Café](./examples/cafe_bot.py) - Get an overview of the design which lies inside Pyrubrum while interacting with multiple commands and pages.
   - [Calendar](./examples/calendar_bot.py) - Get what day of the week a day is by simply choosing a year, a month and a day while discovering the potential of Pyrubrum page menus.
   - [Hitchhiker](./examples/hitchhiker_bot.py) - Come to know how media are handled with Pyrubrum and...[get an existential question answered](https://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy#The_Answer_to_the_Ultimate_Question_of_Life,_the_Universe,_and_Everything_is_42).
   - [Sample](./examples/sample_bot.py) - Interact with inline menus while understanding how Pyrubrum works.

### Changelog

> See [CHANGELOG.md](./CHANGELOG.md).
> Find new features in [FEATURES.md](./FEATURES.md).

### Commit messages

> See [Conventional Commits](https://www.conventionalcommits.org).

### Contributing

> See [CONTRIBUTING.md](./CONTRIBUTING.md).

### Versioning

> See [PEP 440](https://www.python.org/dev/peps/pep-0440/).

### Thanks

   - [veggero/tytg](https://github.com/veggero/tytg) for giving me the idea of developing a simple framework with which you can code a folder-like bot.
   - [IlhomBahoraliev/pyromenu](https://github.com/IlhomBahoraliev/pyromenu) for letting me understand that an object-oriented library would make the difference in developing this project.

### Branding

> See [hearot/pyrubrum-assets](https://github.com/hearot/pyrubrum-assets).

### Copyright & License

- Copyright (C) 2020 [Hearot](https://github.com/hearot).
- Licensed under the terms of the [GNU General Public License v3 (GPLv3)](./LICENSE).
