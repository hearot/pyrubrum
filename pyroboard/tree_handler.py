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
from .base_handler import BaseHandler, pass_handler
from .node import Node, Optional
from dataclasses import dataclass
from pyrogram import Client, MessageHandler
from typing import Any, Dict, List, Tuple


@dataclass
class TreeHandler(BaseHandler):
    main_node: Node

    def get_family(self, unique_id: int) -> Tuple[Optional[BaseMenu],
                                                  Optional[List[BaseMenu]]]:
        return self.main_node.get_family(unique_id, None)

    def get_menus(self) -> List[BaseMenu]:
        return self.main_node.get_menus()

    def setup(self, client: Client):
        BaseHandler.setup(self, client)

        client.add_handler(
            MessageHandler(pass_handler(
                self.main_node.menu.process_text, self)))


def process_node(menus: Dict[BaseMenu, Any], parent: Node):
    for menu in menus:
        node = Node(menu)
        parent.add_child(node)

        if isinstance(menus[menu], dict):
            process_node(menus[menu], node)


def transform_dict(menus: Dict[BaseMenu, Any]) -> Node:
    main_node = Node(list(menus)[0])
    main_value = list(menus.values())[0]

    if main_value:
        process_node(main_value, main_node)

    return main_node
