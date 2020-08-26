# Pyrubrum - An intuitive framework for creating Telegram bots
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyrubrum.
#
# Pyrubrum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrubrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyrubrum. If not, see <https://www.gnu.org/licenses/>.

from typing import List, Set, Union

from environs import Env
from pyrogram import Client

from pyrubrum import (
    DeepLinkMenu,
    DictDatabase,
    Element,
    Menu,
    Node,
    PageMenu,
    ParameterizedHandler,
    RedisDatabase,
    transform,
)

try:
    from redis import Redis
except (ImportError, ModuleNotFoundError):
    pass

drinks = [
    "Beer",
    "Cider",
    "Coffee",
    "Coke",
    "French wine",
    "Gin",
    "Hard soda",
    "Irish beer",
    "Italian wine",
    "Liquor",
    "Water",
    "Wine",
]
snacks = [
    "Bubblegum",
    "Candies",
    "Chocolate bar",
    "Crisps",
    "Cracker nuts",
    "Crêpe",
    "Pancake",
    "Pizza",
    "Pretzel",
    "Waffle",
]


def make_elements(elements: List[str]) -> List[Element]:
    return [Element(name, index) for index, name in enumerate(elements)]


tree = transform(
    {
        Menu(
            "Start",
            "start",
            "ℹ️ Have a drink or a snack by saying /drink or /snack",
            default=True,
        ): [
            DeepLinkMenu("🍷 Drink", "link_drink", "drink"),
            DeepLinkMenu("🍬 Snack", "link_snack", "snack"),
        ],
        PageMenu(
            "Drink",
            "drink",
            "🍷 Choose the drink you want!",
            make_elements(drinks),
            deep_link=True,
        ): {Menu("After drink choice", "drink_chosen", "🍹 Here you go!")},
        PageMenu(
            "Snack",
            "snack",
            "🍬 Choose the snack you want!",
            make_elements(snacks),
            deep_link=True,
        ): {Menu("After snack choice", "snack_chosen", "🥨 Here you go!")},
    }
)


def main(
    api_hash: str,
    api_id: int,
    bot_token: str,
    database: Union[DictDatabase, RedisDatabase],
    session_name: str,
    tree: Set[Node],
):
    bot = Client(
        session_name, api_hash=api_hash, api_id=api_id, bot_token=bot_token
    )

    handler = ParameterizedHandler(tree, database)
    handler.setup(bot)

    bot.run()


if __name__ == "__main__":
    env = Env()
    env.read_env()

    api_hash = env("API_HASH")
    api_id = env.int("API_ID")
    bot_token = env("BOT_TOKEN")
    session_name = env("SESSION_NAME")

    if env.bool("USE_REDIS", False):
        db = env.int("REDIS_DB")
        host = env("REDIS_HOST")
        port = env.int("REDIS_PORT")
        database = RedisDatabase(Redis(host=host, port=port, db=db))
    else:
        database = DictDatabase()

    main(api_hash, api_id, bot_token, database, session_name, tree)
