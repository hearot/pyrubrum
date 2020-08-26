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
from typing import Iterable, Optional, Set, Tuple

from pyrogram import Client
from pyrogram.filters import Filter, create
from pyrogram.handlers import MessageHandler

from pyrubrum.menus import BaseMenu
from pyrubrum.tree import Node

from .base_handler import BaseHandler, pass_handler

DEEP_LINK_FILTER_TEMPLATE = "/start %s"


def command_filter(command: str) -> Filter:
    """Generate a filter that matches all the text messages following this
    pattern::

        /[COMMAND]

    Where ``COMMAND`` is the provided command. Unlike `Filters.command
    <pyrogram.Filters.command>`, it does not match any deep-linked or
    parameterized command.

    Parameters:
        command (str): The command that has to be matched, without
        the prefix ``/``.

    Returns:
        Filter: The generated filter.
    """
    return create(lambda _, __, m: m.text == "/" + command, "DeepLinkFilter")


def deep_link_filter(payload: str) -> Filter:
    """Generate a filter that matches all the text messages following this
    pattern::

        /start [PAYLOAD]

    Where ``PAYLOAD``is the provided payload.

    Parameters:
        payload (str): The payload that has to be matched.

    Returns:
        Filter: The generated filter.
    """
    match = DEEP_LINK_FILTER_TEMPLATE % payload
    return create(lambda _, __, m: m.text == match, "DeepLinkFilter")


class Handler(BaseHandler):
    """Implementation of a simple handler for non-parameterized menus which has
    got, by definition, multiple :term:`top-level nodes <Top-level node>`
    whose linked menus are displayed to the user whenever a message is being
    handled and matches one of their filters.

    Parameters:
        nodes (Set[Node]): The :term:`top-level nodes <Top-level node>`,
            which represent the text commands that are available to the user.

    Note:
        In order to make use of parameterized menus (e.g. `PageMenu`) or to
        pass parameters between menus, you will have to use an handler which
        supports such feature (e.g. `ParameterizedHandler`).
    """

    def __init__(self, nodes: Set[Node]):
        self.nodes = nodes

    @lru_cache()
    def get_family(
        self, menu_id: str
    ) -> Tuple[Optional[BaseMenu], Optional[Iterable[BaseMenu]]]:
        """Retrieve the menus which are linked to both parent and children of the
        :term:`top-level nodes <Top-level node>` of this instance if this
        instance matches the provided identifier. Otherwise it will search the
        menu matching it in the children of the
        :term:top-level nodes <Top-level node>` and will return their own
        families, if matched. On failure, it will return a tuple of length two
        filled with null values (i.e. ``None``).

        Parameters:
            menu_id (str): The identifier which must be matched.

        Returns:
            Tuple[Optional[BaseMenu], Optional[Iterable[BaseMenu]]]: A tuple of
            length two, whose first element is the parent node of the
            matched node while the second one is a tuple of all its children
            If no `Node` is found, the tuple will be filled with null
            values (i.e. ``None``).
        """
        for node in self.nodes:
            family = node.get_family(menu_id, None)

            if family[0] or family[1]:
                return family

        return (None, None)

    @lru_cache(maxsize=1)
    def get_menus(self) -> Set[BaseMenu]:
        """Retrieve the set of all the menus which are linked to the nodes belonging
        to the descent of the :term:`top-level nodes <Top-level node>` of this
        class (i.e. the children, the children of the children, etc...). In
        other words, it retrieves all the menus which were defined at the
        initialization of this instance.

        Returns:
            Set[BaseMenu]: The set of all the retrieved menus.
        """
        menus = set()

        for node in self.nodes:
            menus |= node.get_menus()

        return menus

    def setup(self, client: Client):
        """Set up a client instance by adding filters for handling callbacks and
        messages. If there is a default menu, it adds it using
        `MessageHandler <pyrogram.MessageHandler>`.

        Parameters:
            client (Client): The client you are setting up. It must be a bot
                instance in order to work.
        """
        BaseHandler.setup(self, client)
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
                    pass_handler(node.menu.on_message, self),
                    node.menu.message_filter,
                )
            )

        if default_menu:
            client.add_handler(
                MessageHandler(pass_handler(default_menu.on_message, self))
            )
