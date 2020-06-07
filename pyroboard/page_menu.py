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
from typing import Any, Callable, Dict, List, Optional, Union


@dataclass(eq=False, init=False, repr=True)
class PageMenu(TreeMenu):
    items: Union[List[Element],
                 Callable[[ParameterizedTreeHandler, Client,
                           Union[CallbackQuery, Message],
                           Dict[str, Any]],
                          List[Element]]]
    limit_page: Optional[int] = 4
    next_page_button_text: Optional[str] = "▶️"
    previous_page_button_text: Optional[str] = "◀️"

    def __init__(self, name: str,
                 menu_id: str,
                 content: Union[InputMedia, str],
                 items: Union[List[Element],
                              Callable[[ParameterizedTreeHandler, Client,
                                        Union[CallbackQuery, Message],
                                        Dict[str, Any]],
                                       List[Element]]],
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

    def keyboard(self, tree: ParameterizedTreeHandler,
                 client: Client,
                 context: Union[CallbackQuery,
                                Message],
                 parameters: Dict[str, Any]) -> InlineKeyboardMarkup:
        parent, children = tree.get_family(self.menu_id)

        keyboard = []
        items = []
        page_id = 'page_' + self.menu_id

        if page_id not in parameters:
            parameters[page_id] = 0

        if 'same_menu' in parameters and parameters['same_menu']:
            parameters[page_id] = int(parameters['element_id'])

        if children:
            page_item_menu = children.pop(0)

            if callable(self.items):
                items = self.items(tree, client,
                                   context, parameters)
            elif isinstance(self.items, list):
                items = self.items
            else:
                raise TypeError("items must be either callable or a list")

            elements = items[
                parameters[page_id]*self.limit_page:][:self.limit_page]

            keyboard = [[Button(
                element.name, page_item_menu.menu_id,
                parameters,
                element.element_id) for element in
                        elements[i:i+self.limit]] for i in
                        range(0, len(elements), self.limit)]

        if children:
            keyboard += [[child.button(tree, client,
                                       context, parameters) for child in
                         children[i:i+self.limit]] for i in
                         range(0, len(children), self.limit)]

        teleport_row = []

        if parameters[page_id] > 0:
            previous_page_button = Button(
                self.previous_page_button_text,
                self.menu_id,
                parameters.copy(),
                parameters[page_id]-1,
                True)

            if self.menu_id + "_id" in parameters:
                previous_page_button.parameters[
                    self.menu_id + "_id"] = parameters[self.menu_id + "_id"]

            teleport_row.append(previous_page_button)

        if (parameters[page_id]+1)*self.limit_page < len(items):
            next_page_button = Button(
                self.next_page_button_text,
                self.menu_id,
                parameters.copy(),
                parameters[page_id]+1,
                True)

            if self.menu_id + "_id" in parameters:
                next_page_button.parameters[
                    self.menu_id + "_id"] = parameters[self.menu_id + "_id"]

            teleport_row.append(next_page_button)

        if teleport_row:
            keyboard += [teleport_row]

        if parent:
            parent_button = parent.button(tree, client, context, parameters)
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
