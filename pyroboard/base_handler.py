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

from pyrogram import Client
from typing import Any, Callable


class BaseHandler:
    def setup(self, client: Client):
        raise NotImplementedError


def pass_handler(func: Callable[[Client, Any], None],
                 handler: BaseHandler) -> Callable[[Client, Any], None]:
    def process(client: Client, context):
        func(handler, client, context)

    return process
