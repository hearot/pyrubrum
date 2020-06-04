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

from .button import Button
from .element import Element
from .keyboard import Keyboard
from .page_item_menu import PageItemMenu # noqa
from .parameterized_tree_handler import ParameterizedTreeHandler
from .tree_menu import TreeMenu
from dataclasses import dataclass
from pyrogram import (CallbackQuery, Client,
                      InlineKeyboardMarkup,
                      InputMedia, Message)
from typing import List, Optional, Union


@dataclass(eq=False, init=False, repr=True)
class PageMenu(TreeMenu):
    items: List[Element]
    limit_page: Optional[int] = 4
    next_page_button_text: Optional[str] = "▶️"
    previous_page_button_text: Optional[str] = "◀️"

    def __init__(self, name: str,
                 menu_id: str,
                 content: Union[InputMedia, str],
                 items: List[Element],
                 back_button_text: Optional[str] = "🔙",
                 limit: Optional[int] = 2,
                 limit_page: Optional[int] = 4,
                 next_page_button_text: Optional[str] = "▶️",
                 previous_page_button_text: Optional[str] = "◀️"):
        TreeMenu.__init__(self, name, menu_id, content,
                          back_button_text=back_button_text,
                          limit=limit)
        self.items = items
        self.limit_page = limit_page
        self.next_page_button_text = next_page_button_text
        self.previous_page_button_text = previous_page_button_text

    def get_items(self) -> List[Element]:
        return self.items

    def keyboard(self, tree: ParameterizedTreeHandler,
                 client: Client,
                 context: Union[CallbackQuery,
                                Message],
                 page=0, **_) -> InlineKeyboardMarkup:
        parent, children = tree.get_family(self.menu_id)

        keyboard = []
        items = []

        if children:
            page_item_menu = None

            for index, child in enumerate(children):
                if isinstance(child, PageItemMenu):
                    page_item_menu = child
                    children = children[index+1:]
                    break

            if page_item_menu:
                items = self.get_items()
                elements = items[page*self.limit_page:][:self.limit_page]

                keyboard = [[Button(
                    element.name, page_item_menu.menu_id,
                    page=page, element_id=element.element_id) for element in
                            elements[i:i+self.limit]] for i in
                            range(0, len(elements), self.limit)]

        if children:
            keyboard += [[child.button(tree, client,
                                       context) for child in
                         children[i:i+self.limit]] for i in
                         range(0, len(children), self.limit)]

        teleport_row = []

        if page > 0:
            teleport_row.append(
                Button(self.previous_page_button_text,
                       self.menu_id,
                       page=page-1))

        if (page+1)*self.limit_page < len(items):
            teleport_row.append(
                Button(self.next_page_button_text,
                       self.menu_id,
                       page=page+1))

        if teleport_row:
            keyboard += [teleport_row]

        if parent:
            parent_button = parent.button(tree, client, context)
            parent_button.name = self.back_button_text

            keyboard = keyboard + [[parent_button]]

        if isinstance(context, Message):
            return (Keyboard(keyboard, tree,
                    str(context.message_id) +
                    str(context.from_user.id))
                    if keyboard else None)
        elif isinstance(context, CallbackQuery):
            return (Keyboard(keyboard, tree,
                    context.id) if keyboard else None)
