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
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

from pyrogram import CallbackQuery
from pyrogram import Client
from pyrogram import InlineKeyboardMarkup
from pyrogram import InputMedia
from pyrogram import Message

from .base_menu import BaseMenu
from .handler import Handler
from .keyboard import Keyboard


@dataclass(eq=False, init=False, repr=True)
class Menu(BaseMenu):
    content: Union[
        Union[InputMedia, str],
        Callable[
            [Handler, Client, Union[CallbackQuery, Message], Dict[str, Any]],
            Union[InputMedia, str],
        ],
    ]
    back_button_text: Optional[str] = "🔙"
    limit: Optional[int] = 2

    def __init__(
        self,
        name: str,
        menu_id: str,
        content: Union[
            Union[InputMedia, str],
            Callable[
                [
                    Handler,
                    Client,
                    Union[CallbackQuery, Message],
                    Dict[str, Any],
                ],
                Union[InputMedia, str],
            ],
        ],
        back_button_text: Optional[str] = "🔙",
        limit: Optional[int] = 2,
    ):
        BaseMenu.__init__(self, name, menu_id)
        self.back_button_text = back_button_text
        self.content = content
        self.limit = limit

    def get_content(
        self,
        tree: Handler,
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Dict[str, Any],
    ) -> Union[InputMedia, str]:
        if callable(self.content):
            return self.content(tree, client, context, parameters)

        return self.content

    def preliminary(
        self,
        tree: Handler,
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Dict[str, Any],
    ):
        pass

    def on_callback(
        self,
        tree: Handler,
        client: Client,
        callback: CallbackQuery,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        if not parameters:
            parameters = {}

        self.preliminary(tree, client, callback, parameters)
        content = self.get_content(tree, client, callback, parameters)

        if isinstance(content, InputMedia):
            callback.edit_message_media(
                content,
                reply_markup=self.keyboard(tree, client, callback, parameters),
            )
        elif isinstance(content, str):
            callback.edit_message_text(
                content,
                reply_markup=self.keyboard(tree, client, callback, parameters),
            )
        else:
            raise TypeError("content must be of type InputMedia or str")

    def keyboard(
        self,
        tree: Handler,
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Dict[str, Any],
    ) -> InlineKeyboardMarkup:
        parent, children = tree.get_family(self.menu_id)
        children = list(children) if children else []

        keyboard = []

        if children:
            keyboard = [
                [
                    child.button(tree, client, context, parameters)
                    for child in children[i : i + self.limit]
                ]
                for i in range(0, len(children), self.limit)
            ]

        if parent:
            parent_button = parent.button(tree, client, context, parameters)
            parent_button.name = self.back_button_text

            keyboard = keyboard + [[parent_button]]

        if isinstance(context, Message):
            return (
                Keyboard(
                    keyboard,
                    tree,
                    str(context.message_id) + str(context.from_user.id),
                )
                if keyboard
                else None
            )
        elif isinstance(context, CallbackQuery):
            return Keyboard(keyboard, tree, context.id) if keyboard else None

    def on_message(
        self,
        tree: Handler,
        client: Client,
        message: Message,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        if not parameters:
            parameters = {}

        self.preliminary(tree, client, message, parameters)
        content = self.get_content(tree, client, message, parameters)

        if isinstance(content, InputMedia):
            message.reply_cached_media(
                file_id=content.media,
                file_ref=content.file_ref,
                caption=content.caption,
                reply_markup=self.keyboard(tree, client, message, parameters),
            )
        elif isinstance(content, str):
            message.reply_text(
                content,
                reply_markup=self.keyboard(tree, client, message, parameters),
            )
        else:
            raise TypeError("content must be of type InputMedia or str")
