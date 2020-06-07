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

from .database.base_database import BaseDatabase
from .handler import Handler
from .node import Node
from .parameterized_base_handler import (ParameterizedBaseHandler,
                                         pass_handler_and_clean)
from dataclasses import dataclass
from pyrogram import Client, MessageHandler


@dataclass(eq=False, init=False, repr=True)
class ParameterizedHandler(Handler, ParameterizedBaseHandler):
    def __init__(self, main_node: Node,
                 database: BaseDatabase):
        Handler.__init__(self, main_node)
        ParameterizedBaseHandler.__init__(self, database)

    def setup(self, client: Client):
        ParameterizedBaseHandler.setup(self, client)

        client.add_handler(
            MessageHandler(
                pass_handler_and_clean(
                    self.main_node.menu.on_message, self)))
