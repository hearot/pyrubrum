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

from hashlib import md5
from json import JSONDecodeError
from typing import List

from pyrogram import Client
from pyrogram.filters import Filter, create
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import CallbackQuery, InlineKeyboardButton

from pyrubrum.database import BaseDatabase
from pyrubrum.database.errors import DatabaseError
from pyrubrum.keyboard import Button
from pyrubrum.types import Types

from .base_handler import NULL_POINTER, BaseHandler

try:
    import orjson as json  # noqa
except (ImportError, ModuleNotFoundError):
    import json


class ParameterizedBaseHandler(BaseHandler):
    """Basic implementation of an handler which has got, by definition, a database,
    with which it is able to perform
    :term:`parameterization <Parameterization>` (i.e. it supports parameters).

    The purpose of this class is to give a general interface for an handler
    which supports parameterization, as it doesn't implement anything except
    for a basic setup of the client (see `setup`) and a filter that allows the
    recognition of parameterized queries (see `filter`).

    Parameters:
        database (BaseDatabase): The storage for all the query parameters.
            It is used to pass parameters between menus.
    """

    def __init__(self, database: BaseDatabase):
        self.database = database

    def filter(self, menu_id: str) -> Filter:
        """Generate a function which is used by `CallbackQueryHandler` in order to
        filter callback queries relying on the content of the provided menu
        identifier.

        The content of the callback query is always a MD5 hash which behaves
        as the key for the parameters that are associated to the query the
        user made.

        If the identifier of the chat from which the query was sent does not
        match the one defined in the retrieved parameters, the callback is
        considered invalid.

        The filter returns ``True`` if the query is valid and matches
        ``menu_id``. Otherwise, it returns ``False``.

        Parameters:
            menu_id (str): The unique identifier of the menu that has to be
                matched.

        Returns:
            Filter: The function that gets called whenever a callback query is
            being handled.
        """

        def func(_, __, callback: CallbackQuery):
            if not hasattr(callback, "_result_data"):
                try:
                    callback._result_data = json.loads(
                        self.database.get(callback.data)
                    )

                    if (
                        callback._result_data["from_chat_id"]
                        == callback.message.chat.id
                    ):
                        self.database.delete(callback.data)
                except (DatabaseError, JSONDecodeError):
                    return False

            if (
                callback._result_data["from_chat_id"]
                != callback.message.chat.id
            ):
                return False

            if callback._result_data["menu_id"] == menu_id:
                callback.parameters = callback._result_data

                if (
                    not callback.parameters["same_menu"]
                    and callback.parameters["element_id"]
                ):
                    callback.parameters[menu_id + "_id"] = callback.parameters[
                        "element_id"
                    ]

                return True

            return False

        return create(func, "ParameterizedCallbackData")

    def process_keyboard(
        self,
        keyboard: List[List[Button]],
        callback_query_id: str,
        chat_id: int,
    ) -> List[List[InlineKeyboardButton]]:
        """Given a list which represents an inline keyboard and a
        unique identifier for the callback, generate a Pyrogram-compatible
        inline keyboard.

        It generates a MD5 hash key for each button by following this pattern::

            [CALLBACK_QUERY_ID][MENU_ID][ELEMENT_ID]

        After having generated a key, it sets it to be equal, inside the
        database, to the parameters of the button, which have been
        previously converted to JSON and include ``from_chat_id``, the
        identifier of the chat from which the query was sent, ``element_id``,
        ``menu_id`` and ``same_menu``.

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

        processed_keyboard = []

        for row in keyboard:
            processed_row = []
            processed_keyboard.append(processed_row)

            for button in row:
                if button.link:
                    processed_row.append(
                        InlineKeyboardButton(button.name, url=button.link)
                    )
                    continue

                if button.menu_id == NULL_POINTER:
                    processed_row.append(
                        InlineKeyboardButton(
                            button.name, callback_data=NULL_POINTER
                        )
                    )
                    continue

                key = md5(
                    (
                        str(callback_query_id)
                        + button.menu_id
                        + str(button.element_id)
                    ).encode("utf-8")
                ).hexdigest()

                content = (
                    button.parameters
                    if isinstance(button.parameters, dict)
                    else {}
                )

                content.update(
                    {
                        "from_chat_id": chat_id,
                        "element_id": button.element_id,
                        "menu_id": button.menu_id,
                        "same_menu": button.same_menu,
                    }
                )

                processed_row.append(
                    InlineKeyboardButton(button.name, callback_data=key)
                )

                self.database.set(key, json.dumps(content))

        return processed_keyboard

    def setup(self, client: Client):
        """Make all the defined menus reachable by the client by adding handlers that
        catch all their identifiers to it. It adds support to parameterization
        by applying `ParameterizedBaseHandler.filter` to all the handled
        callback queries. It also calls `pass_parameterized_handler`, which
        lets the callback functions get this handler as argument and deletes
        handled callback queries from the database relying on the passed
        identifiers.

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
                    pass_parameterized_handler(menu.on_callback, self),
                    self.filter(menu.menu_id),
                )
            )


def pass_parameterized_handler(
    func: Types.Callback, handler: ParameterizedBaseHandler
) -> Types.PyrogramCallback:
    """Generate a function which, whenever it is called, subsequently calls
    `callback`, passing the handler from which this object was generated and
    the retrieved parameters (it creates an empty dictionary if non existent).
    It requires a subclass of `ParameterizedBaseHandler` to be
    provided in order to work.

    Parameters:
        callback (Types.Callback): The callback function which
            automatically gets called by the generated function.
        handler (ParameterizedBaseHandler): The handler object which made
            use of this function in order to provide this one as a callback
            to a Pyrogram handler.

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
        if isinstance(context, CallbackQuery):
            func(handler, client, context, context.parameters)
        else:
            func(handler, client, context, {})

    return on_callback
