# Pyroboard - Keyboard manager for Pyrogram
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyroboard.
#
# Pyroboard is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyroboard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyroboard. If not, see <http://www.gnu.org/licenses/>.

from .base_handler import BaseHandler, pass_handler
from dataclasses import dataclass
from json import JSONDecodeError
from pyrogram import (Client, CallbackQueryHandler, # noqa
                      CallbackQuery, MessageHandler)
from pyrogram.client.filters.filters import create

try:
    import orjson as json # noqa
except ImportError:
    import json # noqa


@dataclass(eq=False, init=False, repr=True)
class ParameterizedHandler(BaseHandler):
    separator: str = "|"

    def __init__(self, separator: str = "|"):
        self.separator = separator

    @staticmethod
    def filter(unique_str: str, separator: str):
        def func(flt, callback: CallbackQuery):
            callback.matches = {}

            if callback.data == unique_str:
                return True

            if callback.data.startswith(unique_str + separator):
                try:
                    callback.matches = json.loads(
                        callback.data[len(unique_str) + len(separator):])
                    return True
                except JSONDecodeError:
                    return False

            return False

        return create(func, "ParameterizedCallbackData")

    def parameterize(self, unique_str: str, **kwargs) -> str:
        return self.separator.join(
            [unique_str, json.dumps(kwargs)])

    def setup(self, client: Client):
        for menu in self.get_menus():
            client.add_handler(CallbackQueryHandler(
                pass_handler(menu.on_callback, self),
                ParameterizedHandler.filter(
                    menu.unique_id, self.separator)))
