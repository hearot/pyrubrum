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

from .button import Button, clean_parameters
from .keyboard import Keyboard
from .parameterized_tree_handler import ParameterizedTreeHandler
from .tree_menu import TreeMenu
from dataclasses import dataclass
from pyrogram import (Client, CallbackQuery,
                      InlineKeyboardMarkup, Message)
from typing import Union


@dataclass(eq=False, init=False, repr=True)
class PageItemMenu(TreeMenu):
    def keyboard(self, tree: ParameterizedTreeHandler,
                 client: Client,
                 context: Union[CallbackQuery,
                                Message],
                 page=0, **kwargs) -> InlineKeyboardMarkup:
        parent, children = tree.get_family(self.menu_id)

        if isinstance(context, Message):
            raise TypeError("PageItemMenu supports only CallbackQuery")

        keyboard = []

        if children:
            keyboard = [[child.button(tree, client,
                                      context, **kwargs) for child in
                        children[i:i+self.limit]] for i in
                        range(0, len(children), self.limit)]

        if parent:
            kwargs['page'] = page

            parent_button = Button(
                self.back_button_text,
                parent.menu_id,
                **clean_parameters(kwargs))

            keyboard = keyboard + [[parent_button]]

        return (Keyboard(keyboard, tree,
                         context.id) if keyboard else None)
