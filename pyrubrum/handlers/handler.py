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

from functools import lru_cache
from typing import Optional
from typing import Set
from typing import Tuple

from pyrogram import Client
from pyrogram import MessageHandler

from pyrubrum.menus import BaseMenu
from pyrubrum.tree import Node
from .base_handler import BaseHandler
from .base_handler import pass_handler


class Handler(BaseHandler):
    """Implementation of a simple handler for non parameterized menus which has
    got, by definition, a main node whose linked menu is displayed to the user
    whenever a message is being handled.

    Parameters:
        main_node (Node): The node whose linked menu is used when the user
            texts the bot (i.e. when a `Message` object is being handled).
            In other words, it represents the ``/start`` menu.

    Note:
        In order to make use of parameterized menus (e.g. `PageMenu`) or to
        pass parameters between menus, you will have to use an handler which
        supports such feature (e.g. `ParameterizedHandler`).
    """

    def __init__(self, main_node: Node):
        self.main_node = main_node

    @lru_cache
    def get_family(
        self, menu_id: str
    ) -> Tuple[Optional[BaseMenu], Optional[Set[BaseMenu]]]:
        """Retrieve the menus which are linked to both parent and children of the main
        node of this instance if this instance matches the provided identifier.
        Otherwise it will search the menu matching it in its children and
        return its family, if matched. On failure, it will return a tuple of
        length two filled with null values (i.e. ``None``).

        Parameters:
            menu_id (str): The identifier which must be matched.

        Returns:
            Tuple[Optional[BaseMenu], Optional[Set[BaseMenu]]]: A tuple of
            length two, whose first element is the parent node of the
            matched node while the second one is a set of all its children
            If no `Node` is found, the tuple will be filled with null
            values (i.e. ``None``).
        """
        return self.main_node.get_family(menu_id, None)

    @lru_cache(maxsize=1)
    def get_menus(self) -> Set[BaseMenu]:
        """Retrieve the set of all the menus which are linked to the nodes belonging
        to the descent of the main node of this class (i.e. the children, the
        children of the children, etc...). In other words, it retrieves all the
        menus which were defined at the initialization of this instance.

        Returns:
            Set[BaseMenu]: The set of all the retrieved menus.
        """
        return self.main_node.get_menus()

    def setup(self, client: Client):
        """Set up a client instance by adding filters for handling callbacks and
        messages. If a message is being handled, the menu which is linked to
        the main node of this instance will be displayed.

        Parameters:
            client (Client): The client you are setting up. It must be a bot
                instance in order to work.
        """
        BaseHandler.setup(self, client)

        client.add_handler(
            MessageHandler(pass_handler(self.main_node.menu.on_message, self))
        )
