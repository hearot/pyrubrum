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

from calendar import monthrange
from datetime import datetime
from typing import Set, Union

from environs import Env
from pyrogram import Client

from pyrubrum import (
    DictDatabase,
    Element,
    Menu,
    Node,
    PageMenu,
    PageStyle,
    ParameterizedHandler,
    RedisDatabase,
    transform,
)

try:
    from redis import Redis
except (ImportError, ModuleNotFoundError):
    pass


def generate_days(handler, client, context, parameters):
    month = int(parameters["month_id"])
    year = int(parameters["year_id"])

    return [
        Element(str(day + 1), str(day + 1))
        for day in range(monthrange(year, month)[1])
    ]


def generate_months():
    return [Element(str(month + 1), str(month + 1)) for month in range(12)]


def generate_years(start: int, end: int):
    return [Element(str(year), str(year)) for year in range(start, end + 1)]


def tell_about_the_day(handler, client, context, parameters):
    day = int(parameters["day_id"])
    month = int(parameters["month_id"])
    year = int(parameters["year_id"])

    return "📅 " + datetime(year, month, day).strftime("%d/%m/%Y is a %A.")


tree = transform(
    {
        PageMenu(
            "Start",
            "start",
            "📅 Choose a year.",
            generate_years(1970, 2044),
            default=True,
            style=PageStyle(limit=4, limit_items=15),
        ): {
            PageMenu(
                "After year choice",
                "year",
                "📅 Choose a month.",
                generate_months(),
                style=PageStyle(limit=5, limit_items=12),
            ): {
                PageMenu(
                    "After month choice",
                    "month",
                    "📅 Choose a day.",
                    generate_days,
                    style=PageStyle(limit=5, limit_items=31),
                ): {Menu("After day choice", "day", tell_about_the_day)}
            }
        }
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
