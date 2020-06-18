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

import pytest

from pyrubrum import BaseMenu, Node, transform


def generate_menu(num: int) -> BaseMenu:
    return BaseMenu("Menu %d" % num, "menu_%d" % num)


menu_1 = generate_menu(1)
menu_2 = generate_menu(2)
menu_3 = generate_menu(3)
menu_4 = generate_menu(4)

final_node = Node(
    menu_1,
    children=(
        Node(menu_2, children=()),
        Node(menu_3, children=(Node(menu_4, children=()),)),
    ),
)

all_menus = {menu_1, menu_2, menu_3, menu_4}
children_menus = (menu_2, menu_3)

forest = transform({menu_1: {menu_2: None, menu_3: {menu_4}}})
nodes = iter(forest)
node = next(nodes)


def same_node(n1, n2):
    assert isinstance(n1.menu, BaseMenu)
    assert isinstance(n2.menu, BaseMenu)
    assert isinstance(n1.children, tuple)
    assert isinstance(n2.children, tuple)

    if hash(n1) != hash(n2):
        raise ValueError(
            "different hash for either n1 (%d) or n2 (%d)"
            % (hash(n1), hash(n2))
        )

    if hash(n1.menu) != hash(n2.menu):
        raise ValueError(
            "different hash for either n1.menu (%d) or "
            "n2.menu (%d)" % (hash(n1.menu), hash(n2.menu))
        )

    if len(n1.children) != len(n2.children):
        raise ValueError(
            "n1 and n2 do not share the same number of "
            "children (%d vs %d)" % (len(n1.children), hash(n2.children))
        )

    for i1, i2 in zip(n1.children, n2.children):
        same_node(i1, i2)


def test_transform():
    assert isinstance(forest, set)

    with pytest.raises(StopIteration):
        next(nodes)

    same_node(node, final_node)


def test_get_menus():
    got_menus = node.get_menus()

    assert isinstance(got_menus, set)
    assert got_menus == all_menus

    # do twice because to test cache
    got_menus = node.get_menus()

    assert isinstance(got_menus, set)
    assert got_menus == all_menus


def test_get_children_menus():
    got_menus = node.get_children_menus()

    assert isinstance(got_menus, tuple)
    assert got_menus == children_menus
