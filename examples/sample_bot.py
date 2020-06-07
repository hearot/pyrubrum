# Pyrubrum - An intuitive framework for creating Telegram bots
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyrubrum.
#
# Pyrubrum is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrubrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrubrum. If not, see <http://www.gnu.org/licenses/>.

from environs import Env
from pyrogram import Client
from pyrubrum import Handler, Menu, Node, transform_dict

tree = transform_dict(
    {
        Menu("Main", "main", "Hello!"): {
            Menu("About me", "about_me", "I'm just a bot!"),
            Menu("Thoughts", "thoughts",
                 "I'm a bot, I cannot think properly...")
        }
    }
)


def main(api_hash: str, api_id: int, bot_token: str,
         session_name: str, tree: Node):
    bot = Client(session_name, api_hash=api_hash,
                 api_id=api_id, bot_token=bot_token)
    handler = Handler(tree)
    handler.setup(bot)

    bot.run()


if __name__ == "__main__":
    env = Env()
    env.read_env()

    api_hash = env("API_HASH")
    api_id = env.int("API_ID")
    bot_token = env("BOT_TOKEN")
    session_name = env("SESSION_NAME")

    main(api_hash, api_id, bot_token,
         session_name, tree)
