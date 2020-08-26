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

from abc import ABC, abstractmethod
from typing import List, Set

from pyrogram import Client
from pyrogram.filters import Filter, create
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import InlineKeyboardButton

from pyrubrum.keyboard import Button
from pyrubrum.types import Types

NULL_POINTER = "0"


def callback_data_filter(match: str) -> Filter:
    return create(lambda _, __, m: m.data == match, "CallbackDataFilter")


class BaseHandler(ABC):
    """Basic representation of an handler, which is an entity that manages the
    setup of a `Client <pyrogram.Client>` instance (i.e. the bot).

    The purpose of this class is to give a general interface for an handler,
    even if it already implements both a sample setup and a keyboard processing
    function.

    See Also:
        For complete implementations of this class:

        * `Handler`
        * `ParameterizedHandler`

    Note:
        In order to create a subclass or to access this interface, you will
        need to implement the abstract method `get_menus`. Otherwise, you will
        get an error.
    """

    @abstractmethod
    def get_menus(self) -> Set["BaseMenu"]:
        """This abstract method is intended to be implemented as a collector
        of all the menus which were defined while initializing this object.

        Returns:
            Set[BaseMenu]: The set of the menus that were collected during
            the lookup process.
        """
        raise NotImplementedError

    def process_keyboard(
        self,
        keyboard: List[List[Button]],
        callback_query_id: str,
        chat_id: int,
    ) -> List[List[InlineKeyboardButton]]:
        """Given a list which represents an inline keyboard, a unique identifier
        for the callback and one for the chat from which the query was called,
        generate a Pyrogram-compatible inline keyboard.

        Parameters:
            keyboard (List[List[Button]]): The inline keyboard you want to
                process.
            callback_query_id (str): The unique identifier of the callback
                for which the keyboard is generated.
            chat_id (int): The identifier of the chat from which the query has
                been sent.

        Returns:
            List[List[pyrogram.InlineKeyboardButton]]: The generated keyboard
            in a Pyrogram-compatible type.
        """
        return [
            [
                (
                    InlineKeyboardButton(
                        button.name, callback_data=button.menu_id
                    )
                    if not button.link
                    else InlineKeyboardButton(button.name, url=button.link)
                )
                for button in row
            ]
            for row in keyboard
        ]

    def setup(self, client: Client):
        """Make all the defined menus reachable by the client by adding handlers that
        catch all their identifiers to it. It also calls `pass_handler`, which
        lets the callback functions get this handler as argument.

        Parameters:
            client (Client): The client which is being set up.

        Warning:
            The functions the handlers make use of are not set up in the
            same way objects added using Pyrogram handlers are. Pyrubrum
            implements the following pattern::

                callback(handler, client, context, parameters)
        """
        for menu in self.get_menus():
            if menu.is_link:
                continue

            client.add_handler(
                CallbackQueryHandler(
                    pass_handler(menu.on_callback, self),
                    callback_data_filter(menu.menu_id),
                )
            )


def pass_handler(
    callback: Types.Callback, handler: BaseHandler,
) -> Types.PyrogramCallback:
    """Generate a function which, whenever it is called, subsequently calls
    `callback`, passing the handler from which this object was generated.

    Parameters:
        callback (Types.Callback): The callback function which
            automatically gets called by the generated function.
        handler (BaseHandler): The handler object which made use of this
            function in order to provide this one as a callback to a
            Pyrogram handler.

    Returns:
        Types.PyrogramCallback: The function which is being added to
        a Pyrogram handler.

    Warning:
        The functions the handlers make use of are not set up in the
        same way objects added using Pyrogram handlers are. Pyrubrum
        implements the following pattern::

            callback(handler, client, context, parameters)
    """

    def on_callback(client: Client, context):
        callback(handler, client, context)

    return on_callback
