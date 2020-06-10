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

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable
from typing import List
from typing import NewType
from typing import Union

from pyrogram import CallbackQuery
from pyrogram import CallbackQueryHandler
from pyrogram import Client
from pyrogram import Message
from pyrogram import Filters
from pyrogram import InlineKeyboardButton

from .button import Button

Callback = NewType(
    "Callback",
    (
        Union[
            Callable[["BaseHandler", Client, CallbackQuery], None],
            Callable[["BaseHandler", Client, Message], None],
        ]
    ),
)

PyrogramHandlerCallback = NewType(
    "PyrogramHandlerCallback",
    (
        Union[
            Callable[[Client, CallbackQuery], None],
            Callable[[Client, Message], None],
        ]
    ),
)


@dataclass(eq=False, init=False, repr=True)
class BaseHandler(ABC):
    """Basic representation of an handler, which is an entity that manages the
    setup of a `Client` instance (i.e. the bot).

    The purpose of this class is to give a general interface for an handler,
    even if it already implements both a sample setup and a keyboard processing
    function.

    A sample implementation of this interface is `Handler`.

    Note:
        In order to create a subclass or to access this interface, you will
        need to implement the abstract method `get_menus`. Otherwise, you will
        get an error.
    """

    @abstractmethod
    def get_menus(self) -> List["BaseMenu"]:
        """This abstract method is intended to be implemented as a collector
        of all the menus which were defined while initializing this object.

        Returns:
            List[BaseMenu]: The list of the menus that were collected during
                the lookup process.
        """
        raise NotImplementedError

    def process_keyboard(
        self, keyboard: List[List[Button]], callback_query_id: str
    ) -> List[List[InlineKeyboardButton]]:
        """Given a list of a list of buttons which represents an inline keyboard and a
        unique identifier for the callback, generate a Pyrogram-compatible
        inline keyboard.

        Args:
            keyboard (List[List[Button]]): The inline keyboard you want to
                process.
            callback_query_id (str): The unique identifier of the callback
                which the keyboard is generated for.

        Returns:
            List[List[InlineKeyboardButton]]: The generated keyboard in a
                Pyrogram-compatible type.
        """
        return [
            [
                InlineKeyboardButton(
                    button.name, callback_data=button.button_id
                )
                for button in row
            ]
            for row in keyboard
        ]

    def setup(self, client: Client):
        """Make all the defined menus reachable by the client by adding handlers that
        catch all their identifiers to it.

        Args:
            client (Client): The client which is being set up.

        Warning:
            The functions which the handlers make use of are not set up in the
            same way objects defined using Pyrogram decorators are. Pyrubrum
            implements the following pattern:
                ``callback(handler, client, context, parameters)``
        """
        for menu in self.get_menus():
            client.add_handler(
                CallbackQueryHandler(
                    pass_handler(menu.on_callback, self),
                    Filters.callback_data(menu.menu_id),
                )
            )


def pass_handler(
    callback: Callback, handler: BaseHandler,
) -> PyrogramHandlerCallback:
    """Generate a function which, whenever it is called, subsequently calls
    `callback`, passing the handler which this object was generated from.

    Args:
        callback (Callback): The callback function which
            automatically gets called by the generated function.
        handler (BaseHandler): The handler object which made use of this
            function in order to provide it as the callback argument to a
            Pyrogram handler.

    Returns:
        PyrogramHandlerCallback: The function which is being added to
            a Pyrogram handler.

    Warning:
        The functions which the handlers make use of are not set up in the
        same way objects defined using Pyrogram decorators are. Pyrubrum
        implements the following pattern:
            ``callback(handler, client, context, parameters)``
    """

    def on_callback(client: Client, context):
        callback(handler, client, context)

    return on_callback
