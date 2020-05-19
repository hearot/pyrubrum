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

from .parameterized_tree_handler import ParameterizedTreeHandler
from .tree_menu import TreeMenu
from pyrogram import (Client, CallbackQuery,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup, Message)
from typing import Union


class PageItemMenu(TreeMenu):
    def process_keyboard(self, tree: ParameterizedTreeHandler,
                         client: Client,
                         context: Union[CallbackQuery,
                                        Message]) -> InlineKeyboardMarkup:
        parent, children = tree.get_family(hash(self))

        if isinstance(context, Message):
            raise TypeError("PageItemMenu supports only CallbackQuery")

        page = context.matches[0]

        keyboard = []

        if children:
            keyboard = [[child.process_button(tree, client,
                                              context) for child in
                        children[i:i+self.limit]] for i in
                        range(0, len(children), self.limit)]

        if parent:
            parent_button = InlineKeyboardButton(
                self.back_button_text,
                callback_data=tree.parameterize(
                    str(hash(parent)),
                    str(page)
                )
            )

            keyboard = keyboard + [[parent_button]]

        return InlineKeyboardMarkup(keyboard) if keyboard else None
