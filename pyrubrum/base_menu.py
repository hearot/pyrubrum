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

from .base_handler import BaseHandler
from .button import Button
from dataclasses import dataclass
from pyrogram import (CallbackQuery, Client,
                      InlineKeyboardMarkup,
                      InputMedia, Message)
from typing import Any, Dict, Union


@dataclass(eq=False, init=False, repr=True)
class BaseMenu:
    name: str
    menu_id: str

    def __hash__(self):
        return hash(self.menu_id)

    def __init__(self, name: str, menu_id: str):
        self.name = name
        self.menu_id = menu_id

    def get_content(self) -> Union[InputMedia, str]:
        raise NotImplementedError

    def on_callback(self, handler: BaseHandler,
                    client: Client, callback: CallbackQuery,
                    parameters: Dict[str, Any]):
        raise NotImplementedError

    def button(self, handler: BaseHandler, client: Client,
               context: Union[CallbackQuery,
                              Message],
               parameters: Dict[str, Any]) -> Button:
        return Button(self.name, self.menu_id,
                      parameters)

    def keyboard(self, handler: BaseHandler, client: Client,
                 context: Union[CallbackQuery,
                                Message],
                 parameters: Dict[str, Any]) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def on_message(self, handler: BaseHandler,
                   client: Client, message: Message,
                   parameters: Dict[str, Any]):
        raise NotImplementedError
