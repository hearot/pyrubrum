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
from pyrogram import (Client, CallbackQueryHandler, # noqa
                      CallbackQuery, MessageHandler)
from pyrogram.client.filters.filters import create


@dataclass
class ParameterizedHandler(BaseHandler):
    separator: str = "|"

    def setup(self, client: Client):
        for menu in self.get_menus():
            client.add_handler(CallbackQueryHandler(
                pass_handler(menu.process, self),
                parameterized_callback_data_filter(
                    str(hash(menu)), self.separator)))


def parameterized_callback_data_filter(unique_str: str, separator: str):
    def func(flt, callback: CallbackQuery):
        if callback.data == unique_str:
            callback.matches = []
            return True

        if callback.data.startswith(unique_str + separator):
            callback.matches = callback.data[
                                 len(unique_str) +
                                 len(separator):].split(separator)
            return True

        return False

    return create(func, "ParameterizedCallbackData")
