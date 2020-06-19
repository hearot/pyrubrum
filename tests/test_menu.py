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

from pyrubrum import Menu


class FakeContext:
    @staticmethod
    def edit_message_media(*a, **b):
        pass

    @staticmethod
    def edit_message_text(*a, **b):
        pass

    @staticmethod
    def reply_cached_media(*a, **b):
        pass

    @staticmethod
    def reply_text(*a, **b):
        pass


class FakeHandler:
    @staticmethod
    def get_family(*a, **b):
        return (None, None)


context = FakeContext()
handler = FakeHandler()


def test_menu():
    menu = Menu("Test", "test", "test_content")
    menu.on_callback(handler, None, context)
    menu.on_message(handler, None, context)


def test_menu_with_function():
    worked = []

    def get_content(a, b, c, d=None):
        worked.append(1)
        return "test_content"

    menu = Menu("Test", "test", get_content)
    menu.on_callback(handler, None, context)
    menu.on_message(handler, None, context)

    assert len(worked) == 2


def test_preliminary():
    worked = []

    def preliminary(a, b, c, d=None):
        worked.append(1)

    menu = Menu("Test", "test", "test_content", preliminary=preliminary)
    menu.on_callback(handler, None, context)
    menu.on_message(handler, None, context)

    menu = Menu("Test", "test", "test_content", preliminary=[preliminary] * 5)
    menu.on_callback(handler, None, context)
    menu.on_message(handler, None, context)

    menu = Menu("Test", "test", "test_content", preliminary=None)
    menu.on_callback(handler, None, context)
    menu.on_message(handler, None, context)

    assert len(worked) == 12
