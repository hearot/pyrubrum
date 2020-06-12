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

from dataclasses import dataclass

from pyrogram import Client
from pyrogram import MessageHandler

from .database.base_database import BaseDatabase
from .handler import Handler
from .node import Node
from .parameterized_base_handler import ParameterizedBaseHandler
from .parameterized_base_handler import pass_handler_and_clean


@dataclass(eq=False, init=False, repr=True)
class ParameterizedHandler(Handler, ParameterizedBaseHandler):
    """Implementation of an handler which mixes the features of `Handler` and
    `ParameterizedBaseHandler` and has got, by definition, a main node whose
    linked menu is displayed to the user whenever a message is being handled
    and a database with which it is able to perform parameterization (i.e.
    it supports parameters).
    """

    def __init__(self, main_node: Node, database: BaseDatabase):
        """Initialize the object.

        Args:
            main_node (Node): The node whose linked menu is used when the user
                texts the bot (i.e. when a `Message` object is being handled).
                In other words, it represents the ``/start`` menu. See
                `Handler` for more information.
            database (BaseDatabase): The storage for all the query parameters.
                It is used to pass parameters between menus. See
                `ParameterizedBaseHandler` for more information.
        """

        Handler.__init__(self, main_node)
        ParameterizedBaseHandler.__init__(self, database)

    def setup(self, client: Client):
        """Make all the defined menus reachable by the client by adding handlers that
        catch all their identifiers to it. It adds support to parameterization
        by applying ``ParameterizedBaseHandler.filter` to all the handled
        callback queries. It also calls `pass_handler_and_clean`, which lets
        the callback functions get this handler as argument and deletes
        handled callback queries from the database relying on the passed
        identifiers.

        Finally, it makes the main menu (i.e. the menu which is linked to the
        main node) reachable whenever a message is sent to the bot.

        Args:
            client (Client): The client which is being set up.

        Warning:
            The functions the handlers make use of are not set up in the
            same way objects added using Pyrogram handlers are. Pyrubrum
            implements the following pattern:
                ``callback(handler, client, context, parameters)``
        """
        ParameterizedBaseHandler.setup(self, client)

        client.add_handler(
            MessageHandler(
                pass_handler_and_clean(self.main_node.menu.on_message, self)
            )
        )
