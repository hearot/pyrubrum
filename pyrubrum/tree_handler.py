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

from .base_menu import BaseMenu
from .base_handler import BaseHandler, pass_handler
from .node import Node, Optional
from dataclasses import dataclass
from pyrogram import Client, MessageHandler
from typing import Any, Dict, Iterable, List, Tuple, Union


@dataclass(eq=False, init=False, repr=True)
class TreeHandler(BaseHandler):
    main_node: Node

    def __init__(self, main_node: Node):
        self.main_node = main_node

    def get_family(self, menu_id: str) -> Tuple[Optional[BaseMenu],
                                                Optional[List[BaseMenu]]]:
        return self.main_node.get_family(menu_id, None)

    def get_menus(self) -> List[BaseMenu]:
        return self.main_node.get_menus()

    def setup(self, client: Client):
        BaseHandler.setup(self, client)

        client.add_handler(
            MessageHandler(pass_handler(
                self.main_node.menu.on_message, self)))


def on_callback_node(menus: Union[Dict[BaseMenu, Any],
                                  Iterable[BaseMenu]],
                     parent: Node):
    for menu in menus:
        node = Node(menu)
        parent.add_child(node)

        if isinstance(menus, dict) and isinstance(menus[menu], Iterable):
            on_callback_node(menus[menu], node)


def transform_dict(menus: Union[Dict[BaseMenu, Any],
                                Iterable[BaseMenu]]) -> Node:
    main_node = Node(list(menus)[0])
    main_value = list(menus.values())[0] if isinstance(menus, dict) else None

    if main_value:
        on_callback_node(main_value, main_node)

    return main_node
