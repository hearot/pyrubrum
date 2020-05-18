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

from .base_menu import BaseMenu
from .tree_handler import TreeHandler
from dataclasses import dataclass
from pyrogram import (Client, CallbackQuery, InlineKeyboardButton,
                      InlineKeyboardMarkup, InputMedia, Message)
from typing import Optional, Union


@dataclass(frozen=True)
class TreeMenu(BaseMenu):
    content: Union[InputMedia, str]
    limit: Optional[int] = 3
    back_button_text: str = "🔙"

    def get_content(self) -> Union[InputMedia, str]:
        return self.content

    def preliminary(self, tree: TreeHandler, client: Client,
                    context: Union[CallbackQuery, Message]):
        pass

    def process(self, tree: TreeHandler, client: Client,
                callback: CallbackQuery):
        self.preliminary(tree, client, callback)
        content = self.get_content()

        if isinstance(content, InputMedia):
            callback.edit_message_media(
                content, self.process_keyboard(
                    tree, client, callback))
        elif isinstance(content, str):
            callback.edit_message_text(
                content,
                reply_markup=self.process_keyboard(
                    tree, client, callback))
        else:
            raise TypeError("content must be of type InputMedia or str")

    def process_keyboard(self, tree: TreeHandler, client: Client,
                         callback: CallbackQuery) -> InlineKeyboardMarkup:
        parent, children = tree.get_family(hash(self))

        keyboard = []

        if children:
            keyboard = [[child.process_button() for child in
                        children[i:i+self.limit]] for i in
                        range(0, len(children), self.limit)]

        if parent:
            keyboard = keyboard + [[InlineKeyboardButton(
                self.back_button_text,
                callback_data=str(hash(parent)))]]

        return InlineKeyboardMarkup(keyboard) if keyboard else None

    def process_text(self, tree: TreeHandler, client: Client,
                     message: Message):
        self.preliminary(tree, client, message)
        content = self.get_content()

        if isinstance(content, InputMedia):
            raise NotImplementedError  # TODO: handle media
        elif isinstance(content, str):
            message.reply_text(content,
                               reply_markup=self.process_keyboard(
                                   tree, client, message
                               ))
        else:
            raise TypeError("content must be of type InputMedia or str")
