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

from dataclasses import dataclass
from json import JSONDecodeError
from typing import Any
from typing import Callable
from typing import List

from pyrogram import CallbackQuery
from pyrogram import CallbackQueryHandler
from pyrogram import Client
from pyrogram import InlineKeyboardButton
from pyrogram.client.filters.filters import create

from .base_handler import BaseHandler
from .button import Button
from .database.base_database import BaseDatabase

try:
    import orjson as json  # noqa
except (ImportError, ModuleNotFoundError):
    import json


@dataclass(eq=False, init=False, repr=True)
class ParameterizedBaseHandler(BaseHandler):
    database: BaseDatabase

    def __init__(self, database: BaseDatabase):
        self.database = database

    def filter(self, menu_id: str):
        def func(flt, callback: CallbackQuery):
            parameters = callback.data.split()

            if parameters[1] != menu_id:
                return False

            result = self.database.get(parameters[0])

            if result:
                try:
                    content = json.loads(result)

                    if parameters[1] in content:
                        callback.parameters = content[parameters[1]]
                        callback.parameters["callback_query_id"] = parameters[
                            0
                        ]
                        callback.parameters["menu_id"] = parameters[1]

                        if len(parameters) > 2:
                            callback.parameters["element_id"] = parameters[2]

                            if not callback.parameters["same_menu"]:
                                callback.parameters[
                                    parameters[1] + "_id"
                                ] = parameters[2]

                        return True

                    return False
                except JSONDecodeError:
                    return False

            return False

        return create(func, "ParameterizedCallbackData")

    def process_keyboard(
        self, keyboard: List[List[Button]], callback_query_id: str
    ) -> List[List[InlineKeyboardButton]]:
        content = {}

        for row in keyboard:
            for button in row:
                content[button.button_id] = {
                    "callback_query_id": str(callback_query_id),
                    **button.parameters,
                }

        self.database.set(callback_query_id, json.dumps(content))

        return [
            [
                InlineKeyboardButton(
                    button.name,
                    " ".join(
                        map(
                            str,
                            [
                                callback_query_id,
                                button.button_id,
                                button.element_id,
                            ],
                        )
                    )
                    .strip()
                    .rstrip(),
                )
                for button in row
            ]
            for row in keyboard
        ]

    def setup(self, client: Client):
        for menu in self.get_menus():
            client.add_handler(
                CallbackQueryHandler(
                    pass_handler_and_clean(menu.on_callback, self),
                    self.filter(menu.menu_id),
                )
            )


def pass_handler_and_clean(
    func: Callable[[Client, Any], None], handler: ParameterizedBaseHandler
) -> Callable[[Client, Any], None]:
    def on_callback(client: Client, context):
        if isinstance(context, CallbackQuery):
            func(handler, client, context, context.parameters)
            handler.database.delete(context.parameters["callback_query_id"])
        else:
            func(handler, client, context)

    return on_callback
