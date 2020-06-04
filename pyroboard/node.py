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
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass(eq=False, init=False, repr=True)
class Node:
    menu: BaseMenu
    children: Optional[List['Node']] = None

    def __init__(self, menu: BaseMenu,
                 children: Optional[List['Node']] = None):
        if children:
            self.children = children
        else:
            self.children = []

        self.menu = menu

    def add_child(self, node: 'Node'):
        self.children.append(node)

    def get_children_menus(self) -> List[BaseMenu]:
        children = [child.menu for child in self.children]
        return children if children else None

    def get_family(self, menu_id: str,
                   parent: Optional['Node']) -> Tuple[Optional[BaseMenu],
                                                      Optional[
                                                          List[BaseMenu]]]:
        if self.menu.menu_id == menu_id:
            return (parent.menu if isinstance(parent, Node) else None,
                    self.get_children_menus())

        for child in self.children:
            child_menus = child.get_family(menu_id, self)

            if child_menus[0]:
                return child_menus

        return (None, None)

    def get_menus(self) -> List[BaseMenu]:
        menus = [self.menu]

        for child in self.children:
            if child.menu.menu_id != self.menu.menu_id:
                menus += child.get_menus()

        return menus
