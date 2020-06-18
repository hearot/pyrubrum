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

import pytest

from pyrubrum import DeepLinkMenu
from pyrubrum.menus.deep_link_menu import PERMITTED_TYPES, USERNAMES

client_test = "Test client"
username_test = "test_bot"

USERNAMES[hash(client_test)] = username_test

payload = "test_payload"

expected_deep_link = "https://t.me/%s?start=%s" % (username_test, payload)


@pytest.mark.parametrize("deep_type", PERMITTED_TYPES | {"fancytype"})
def test_deep_link_menu(deep_type):
    if deep_type in PERMITTED_TYPES:
        menu = DeepLinkMenu("Test", "test", payload, deep_type)
        menu.button(None, client_test, None)
    else:
        with pytest.raises(ValueError):
            DeepLinkMenu("Test", "test", payload, deep_type)


def test_button():
    menu = DeepLinkMenu("Test", "test", payload)
    button = menu.button(None, client_test, None)

    assert button.link == expected_deep_link
    assert not hasattr(button, "menu_id")
    assert button.name == "Test"


def test_button_with_function():
    menu = DeepLinkMenu("Test", "test", lambda a, b, c, d: payload)
    button = menu.button(None, client_test, None)

    assert button.link == expected_deep_link
    assert not hasattr(button, "menu_id")
    assert button.name == "Test"
