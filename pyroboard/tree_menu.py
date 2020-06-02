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
from pyrogram import (Client, CallbackQuery,
                      InlineKeyboardMarkup, InputMedia,
                      Message)
from typing import Optional, Union


@dataclass(eq=False, init=False, repr=True)
class TreeMenu(BaseMenu):
    content: Union[InputMedia, str]
    back_button_text: Optional[str] = "🔙"
    limit: Optional[int] = 2

    def __init__(self, name: str, unique_id: str,
                 content: Union[InputMedia, str],
                 back_button_text: Optional[str] = "🔙",
                 limit: Optional[int] = 2):
        BaseMenu.__init__(self, name, unique_id)
        self.back_button_text = back_button_text
        self.content = content
        self.limit = limit

    def get_content(self, tree: TreeHandler, client: Client,
                    context: Union[CallbackQuery,
                                   Message],
                    **_) -> Union[InputMedia, str]:
        return self.content

    def preliminary(self, tree: TreeHandler, client: Client,
                    context: Union[CallbackQuery, Message],
                    **_):
        pass

    def on_callback(self, tree: TreeHandler, client: Client,
                    callback: CallbackQuery, **kwargs):
        self.preliminary(tree, client, callback, **kwargs)
        content = self.get_content(tree, client, callback, **kwargs)

        if isinstance(content, InputMedia):
            callback.edit_message_media(
                content, self.keyboard(
                    tree, client, callback, **kwargs))
        elif isinstance(content, str):
            callback.edit_message_text(
                content,
                reply_markup=self.keyboard(
                    tree, client, callback, **kwargs))
        else:
            raise TypeError("content must be of type InputMedia or str")

    def keyboard(self, tree: TreeHandler, client: Client,
                 context: Union[CallbackQuery,
                                Message], **kwargs) -> InlineKeyboardMarkup:
        parent, children = tree.get_family(self.unique_id)

        keyboard = []

        if children:
            keyboard = [[child.button(tree, client,
                                      context, **kwargs) for child in
                        children[i:i+self.limit]] for i in
                        range(0, len(children), self.limit)]

        if parent:
            parent_button = parent.button(tree, client, context, **kwargs)
            parent_button.text = self.back_button_text

            keyboard = keyboard + [[parent_button]]

        return InlineKeyboardMarkup(keyboard) if keyboard else None

    def on_message(self, tree: TreeHandler, client: Client,
                   message: Message):
        self.preliminary(tree, client, message)
        content = self.get_content(tree, client, message)

        if isinstance(content, InputMedia):
            raise NotImplementedError  # TODO: handle media
        elif isinstance(content, str):
            message.reply_text(content,
                               reply_markup=self.keyboard(
                                   tree, client, message
                               ))
        else:
            raise TypeError("content must be of type InputMedia or str")
