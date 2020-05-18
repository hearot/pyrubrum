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


@dataclass(frozen=True)
class BaseMenu:
    name: str

    def get_content(self) -> Union[InputMedia, str]:
        raise NotImplementedError

    def process(self, handler: BaseHandler,
                client: Client, callback: CallbackQuery):
        raise NotImplementedError

    def process_button(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(self.name,
                                    callback_data=str(hash(self)))

    def process_keyboard(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def process_text(self, handler: BaseHandler,
                     client: Client, message: Message):
        raise NotImplementedError
