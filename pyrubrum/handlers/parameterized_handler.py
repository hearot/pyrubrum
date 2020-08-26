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

from typing import Set

from pyrogram import Client
from pyrogram.handlers import MessageHandler

from pyrubrum.database import BaseDatabase
from pyrubrum.tree import Node

from .handler import Handler, command_filter, deep_link_filter
from .parameterized_base_handler import (
    ParameterizedBaseHandler,
    pass_parameterized_handler,
)


class ParameterizedHandler(Handler, ParameterizedBaseHandler):
    """Implementation of an handler which mixes the features of `Handler` and
    `ParameterizedBaseHandler` and has got, by definition, multiple
    :term:`top-level nodes <Top-level node>` whose linked menu are
    displayed to the user whenever a message is being handled and matches
    one of their filters, and a database with which it is possible to
    perform :term:`parameterization <Parameterization>`
    (i.e. it supports parameters).

    Parameters:
        nodes (Set[Node]): The :term:`top-level nodes <Top-level node>`,
            which represent the text commands that are available to the user.
            See `Handler` for more information.
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
        callback queries. It also calls `pass_parameterized_handler`, which
        lets the callback functions get this handler as argument and deletes
        handled callback queries from the database relying on the passed
        identifiers.

        Finally, it makes the :term:`top-level menus <Top-level menu>`
        reachable whenever a message is sent to the bot and matches one of
        their filters.

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
                node.menu.message_filter = command_filter(node.menu.menu_id)

            if node.menu.deep_link:
                node.menu.message_filter |= deep_link_filter(node.menu.menu_id)

            if node.menu.default:
                default_menu = node.menu

            client.add_handler(
                MessageHandler(
                    pass_parameterized_handler(node.menu.on_message, self),
                    node.menu.message_filter,
                )
            )

        if default_menu:
            client.add_handler(
                MessageHandler(
                    pass_parameterized_handler(default_menu.on_message, self)
                )
            )
