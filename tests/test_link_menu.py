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

from pyrubrum import LinkMenu

example_link = "https://example.com"
example_name = "Example"


def test_button():
    link = LinkMenu(example_name, "test", example_link)
    button = link.button(None, None, None)

    assert button.link == example_link
    assert not hasattr(button, "menu_id")
    assert button.name == example_name


def test_button_with_function():
    link = LinkMenu(example_name, "test", lambda a, b, c, d: example_link)
    button = link.button(None, None, None)

    assert button.link == example_link
    assert not hasattr(button, "menu_id")
    assert button.name == example_name
