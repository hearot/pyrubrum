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

from .base_handler import BaseHandler
from dataclasses import dataclass
from pyrogram import (CallbackQuery, Client,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      InputMedia, Message)
from typing import Union


@dataclass(eq=False, init=False, repr=True)
class BaseMenu:
    name: str
    unique_id: str

    def __hash__(self):
        return hash(self.unique_id)

    def __init__(self, name: str, unique_id: str):
        self.name = name
        self.unique_id = unique_id

    def get_content(self) -> Union[InputMedia, str]:
        raise NotImplementedError

    def on_callback(self, handler: BaseHandler,
                    client: Client, callback: CallbackQuery):
        raise NotImplementedError

    def button(self, handler: BaseHandler, client: Client,
               context: Union[CallbackQuery,
                              Message]) -> InlineKeyboardButton:
        return InlineKeyboardButton(self.name,
                                    callback_data=self.unique_id)

    def keyboard(self, handler: BaseHandler, client: Client,
                 context: Union[CallbackQuery,
                                Message]) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def on_message(self, handler: BaseHandler,
                   client: Client, message: Message):
        raise NotImplementedError
