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

from functools import lru_cache
from typing import Any, Dict, Iterable, Optional, Set, Tuple, Union

from pyrubrum.menus import BaseMenu

Family = Tuple[Optional[BaseMenu], Optional[Set[BaseMenu]]]
MenuIterable = Union[Dict[BaseMenu, Any], Iterable[BaseMenu]]


class Node:
    """Representation of a single object in a tree, which might have defined a
    parent (i.e. the `Node` object it is child of) and a set of other nodes,
    which are its children. Each `Node` instance is linked to a subclass of
    `BaseMenu`.

    Parameters:
        menu (BaseMenu): The menu this node is being linked to.
        children (Optional[Set[Node]]): The nodes whose parent is going
            to be this instance. Defaults to ``None``, which makes the
            children set an empty one.
    """

    def __hash__(self) -> int:
        """The hash generator for a node, relying on the hash of the linked
        menu.

        Returns:
            int: The hash of the menu which is linked to this instance.
        """
        return hash(self.menu)

    def __init__(self, menu: BaseMenu, children: Optional[Set["Node"]] = None):
        self.children = children if children else tuple()
        self.menu = menu

    def add_child(self, node: "Node"):
        """Add a `Node` instance to the set of children.

        Parameters:
            node (Node): The node which is being added as a child of this
                object.
        """
        self.children += (node,)

    @lru_cache(maxsize=1)
    def get_children_menus(self) -> Iterable[BaseMenu]:
        """Get all the menus that are linked to the children belonging to
        this instance.

        Returns:
            Iterable[BaseMenu]: A tuple that contains all the retrieved menus.
        """
        children = tuple(child.menu for child in self.children)
        return children if children else None

    @lru_cache()
    def get_family(self, menu_id: str, parent: Optional["Node"]) -> Family:
        """Retrieve the menus which are linked to both parent and children of this
        instance if this instance matches the provided identifier. Otherwise it
        will search the menu matching it in its children and return its family,
        if matched. On failure, it will return a tuple of length two filled
        with null values (i.e. ``None``).

        Parameters:
            menu_id (str): The identifier which must be matched.
            parent (Optional[Node]): The parent this ``Node`` comes from.

        Returns:
            Tuple[Optional[BaseMenu], Optional[Tuple[BaseMenu]]]: A tuple of
            length two, whose first element is the parent node of the
            matched node while the second one is a tuple of all its children
            If no `Node` is found, the tuple will be filled with null
            values (i.e. ``None``).
        """
        if self.menu.menu_id == menu_id:
            return (
                parent.menu if isinstance(parent, Node) else None,
                self.get_children_menus(),
            )

        for child in self.children:
            child_menus = child.get_family(menu_id, self)

            if child_menus[0]:
                return child_menus

        return (None, None)

    @lru_cache(maxsize=1)
    def get_menus(self) -> Set[BaseMenu]:
        """Retrieve the set of all the menus which are linked to the nodes belonging
        to the descent of this class (i.e. the children, the children of the
        children, etc...).

        Returns:
            Set[BaseMenu]: The set of all the retrieved menus.
        """
        menus = {self.menu}

        for child in self.children:
            if child.menu.menu_id != self.menu.menu_id:
                menus |= child.get_menus()

        return menus


def recursive_add(menus: MenuIterable, parent: Node):
    """Link the provided menus to `Node` instances and add these ones to a provided
    parent. Finally, for each found value which is iterable, this function is
    called in a recursive way in order to link its elements to its parent
    `Node`.

    Parameters:
        menus (MenuIterable): The provided iterable of the menus which are
            being added to the parent node. If it is a dictionary, the stored
            value for each key, if iterable, will be recursively provided as
            argument to a new call of this function, together with the parent
            node, which is the key.
        parent (Node): The parent the nodes are being added to.
    """
    for menu in menus:
        node = Node(menu)
        parent.add_child(node)

        if isinstance(menus, dict) and isinstance(menus[menu], Iterable):
            recursive_add(menus[menu], node)


def transform(menus: MenuIterable) -> Set[Node]:
    """Transform an iterable compounded of menus into a `Node` object. If a
    dictionary is provided as argument, its values will be transformed as
    well and added as children using ``recursive_add``.

    Parameters:
        menus (Union[Dict[BaseMenu, Any], Iterable[BaseMenu]]): The iterable
            whose elements are `BaseMenu` instances.

    Returns:
        Node: The `Node` object which collects all the menus as children.
    """
    nodes = set()

    for menu in menus:
        node = Node(menu)
        nodes.add(node)

        if isinstance(menus, dict) and menus[menu]:
            recursive_add(menus[menu], node)

    return nodes
