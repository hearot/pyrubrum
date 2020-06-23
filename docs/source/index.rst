Welcome to Pyrubrum
===================

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
            Menu("Start", "start", "Hello!", default=True): [
                Menu("About me", "about_me", "I'm just a bot!"),
                Menu("Thoughts", "thoughts",
                    "I'm a bot, I cannot think properly..."),
            ]
        }
    ))

    handler.setup(bot)
    bot.run()

.. tip::
    If you think something should be added to the documentation, feel free to make a proposal by opening an `issue <https://github.com/hearot/pyrubrum/issues/new?assignees=hearot&labels=enhancement-request&template=feature_request.md&title=%5BFeature%5D>`_ on GitHub.

.. toctree::
    :caption: Quickstart

    quickstart/installation
    quickstart/overview

.. toctree::
    :caption: Examples

    examples/sample
    examples/cafe_bot
    examples/calendar_bot
    examples/hitchhiker_bot
    examples/sample_bot

.. toctree::
    :caption: API Reference
    :hidden:

    api/database/index
    api/database/errors/index
    api/handlers/index
    api/keyboard/index
    api/menus/index
    api/objects/index
    api/styles/index
    api/tree/index
    api/types/index

.. toctree::
    :caption: Meta
    :maxdepth: 1

    Assets <https://github.com/hearot/pyrubrum-assets>
    CHANGELOG
    Code of Conduct <CODE_OF_CONDUCT>
    CONTRIBUTING
    flowchart
    glossary
    license
    Read me <README>
    SECURITY
