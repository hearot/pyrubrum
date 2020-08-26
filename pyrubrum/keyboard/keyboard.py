# Pyrubrum - An intuitive framework for creating Telegram bots
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyrubrum.
#
# Pyrubrum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrubrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyrubrum. If not, see <https://www.gnu.org/licenses/>.

from typing import List

from pyrogram.types import InlineKeyboardMarkup

from .button import Button


class Keyboard(InlineKeyboardMarkup):
    """Simple shortcut for calling `BaseHandler.process_keyboard` and storing the
    processed keyboard in the same object.

    It is useful since it automatically processes the content of buttons
    and, at the same time, behaves like a normal `InlineKeyboardMarkup
    <pyrogram.InlineKeyboardMarkup>` instance.

    Parameters:
        inline_keyboard (List[List[Button]]): The keyboard which is going
            to be converted.
        handler (BaseHandler): The handler from which the function
            `BaseHandler.process_function` is going to be called.
        callback_query_id (str): The unique identifier of the query, which
            will be used to make the call that is made by the inline
            buttons unique.
        chat_id (int): The identifier of the chat from which the query has
            been sent.
    """

    def __init__(
        self,
        inline_keyboard: List[List[Button]],
        handler: "BaseHandler",  # noqa
        callback_query_id: str,
        chat_id: int,
    ):
        super().__init__(
            handler.process_keyboard(
                inline_keyboard, callback_query_id, chat_id
            )
        )
