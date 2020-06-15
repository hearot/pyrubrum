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

from typing import Set

from pyrogram import Client
from pyrogram import Filters
from pyrogram import MessageHandler

from pyrubrum.database import BaseDatabase
from pyrubrum.tree import Node
from .handler import Handler
from .parameterized_base_handler import ParameterizedBaseHandler
from .parameterized_base_handler import pass_handler_and_clean


class ParameterizedHandler(Handler, ParameterizedBaseHandler):
    """Implementation of an handler which mixes the features of `Handler` and
    `ParameterizedBaseHandler` and has got, by definition, multiple top-level
    nodes whose linked menu are displayed to the user whenever a message is
    being handled and matches one of their filters, and a database with which
    it is possible to perform parameterization (i.e. it supports parameters).

        nodes (Set[Node]): The top-level nodes, which represent the text
            commands that are available to the user. See `Handler` for more
            information
        database (BaseDatabase): The storage for all the query parameters.
            It is used to pass parameters between menus. See
            `ParameterizedBaseHandler` for more information.
    """

    def __init__(self, nodes: Set[Node], database: BaseDatabase):
        Handler.__init__(self, nodes)
        ParameterizedBaseHandler.__init__(self, database)

    def setup(self, client: Client):
        """Make all the defined menus reachable by the client by adding handlers that
        catch all their identifiers to it. It adds support to parameterization
        by applying `ParameterizedBaseHandler.filter` to all the handled
        callback queries. It also calls `pass_handler_and_clean`, which lets
        the callback functions get this handler as argument and deletes
        handled callback queries from the database relying on the passed
        identifiers.

        Finally, it makes the top-level menus reachable whenever a message is
        sent to the bot and matches one of their filters.

        Parameters:
            client (Client): The client which is being set up.

        Warning:
            The functions the handlers make use of are not set up in the
            same way objects added using Pyrogram handlers are. Pyrubrum
            implements the following pattern::

                callback(handler, client, context, parameters)
        """
        ParameterizedBaseHandler.setup(self, client)
        default_menu = None

        for node in self.nodes:
            if node.menu.is_link:
                continue

            if not node.menu.message_filter:
                node.menu.message_filter = Filters.command(node.menu.menu_id)

            if node.menu.default:
                default_menu = node.menu

            client.add_handler(
                MessageHandler(
                    pass_handler_and_clean(node.menu.on_message, self),
                    node.menu.message_filter,
                )
            )

        if default_menu:
            client.add_handler(
                MessageHandler(
                    pass_handler_and_clean(default_menu.on_message, self)
                )
            )
