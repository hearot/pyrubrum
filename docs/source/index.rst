Welcome to Pyrubrum
===================

.. toctree::
    :hidden:
    :caption: API Reference

    api/database/index
    api/database/errors/index
    api/handlers/index
    api/menus/index
    api/utils/index

.. raw:: html

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

.. code-block:: python

    from pyrogram import Client
    from pyrubrum import Handler, Menu, transform

    bot = Client(...)

    handler = Handler(transform(
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
