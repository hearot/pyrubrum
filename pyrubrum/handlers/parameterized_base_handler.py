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

from json import JSONDecodeError
from typing import List

from pyrogram import CallbackQuery
from pyrogram import CallbackQueryHandler
from pyrogram import Client
from pyrogram import InlineKeyboardButton
from pyrogram.client.filters.filters import create
from pyrogram.client.filters.filters import Filter

from pyrubrum.keyboard import Button
from pyrubrum.database import BaseDatabase
from pyrubrum.types import Types
from .base_handler import BaseHandler

try:
    import orjson as json  # noqa
except (ImportError, ModuleNotFoundError):
    import json


class ParameterizedBaseHandler(BaseHandler):
    """Basic implementation of an handler which has got, by definition, a database,
    with which it is able to perform parameterization (i.e. it supports
    parameters).

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

        A callback query is valid if its content follows the following
        pattern::

            [CALLBACK_QUERY_ID] [MENU_ID] [ELEMENT_ID, optional]

        If the query that is being handled matches ``MENU_ID``, database is
        queried with the content of ``CALLBACK_QUERY_ID``. If a valid match
        is found, its content is converted from JSON and then parameters are
        collected and stored in ``callback.parameters``.

        If ``ELEMENT_ID`` is provided, ``element_id`` is set to be equal to it
        in ``callback.parameters``. If ``same_menu`` in ``callback.parameters``
        is ``False``, a new key named ``[MENU_ID]_id`` is set to be equal to
        ``ELEMENT_ID`` in ``callback.parameters``.

        The filter returns ``True`` if the query is valid and matches
        ``menu_id``. Otherwise, it returns ``False``.

        Parameters:
            menu_id (str): The unique identifier of the menu that has to be
                matched.

        Returns:
            Filter: The function that gets called whenever a callback query is
            being handled.
        """

        def func(_, callback: CallbackQuery):
            parameters = callback.data.split()

            if parameters[1] != menu_id:
                return False

            result = self.database.get(parameters[0])

            if result:
                try:
                    content = json.loads(result)

                    if parameters[1] in content:
                        callback.parameters = content[parameters[1]]
                        callback.parameters["callback_query_id"] = parameters[
                            0
                        ]
                        callback.parameters["menu_id"] = parameters[1]

                        if len(parameters) > 2:
                            callback.parameters["element_id"] = parameters[2]

                            if not callback.parameters["same_menu"]:
                                callback.parameters[
                                    parameters[1] + "_id"
                                ] = parameters[2]

                        return True

                    return False
                except JSONDecodeError:
                    return False

            return False

        return create(func, "ParameterizedCallbackData")

    def process_keyboard(
        self, keyboard: List[List[Button]], callback_query_id: str
    ) -> List[List[InlineKeyboardButton]]:
        """Given a list of a list of buttons which represents an inline keyboard and a
        unique identifier for the callback, generate a Pyrogram-compatible
        inline keyboard. It also creates a dictionary ``content``, whose keys
        represent the identifiers of the menu collected in the keyboard and
        values their own parameters. Finally, it converts ``content`` to JSON
        and stores it inside the database using the provided query identifier
        as key.

        The returned inline keyboard does not store any parameters. Instead,
        its buttons stores the data needed to get the parameters from the
        database, in accordance with the following pattern::

            [CALLBACK_QUERY_ID] [MENU_ID] [ELEMENT_ID, optional]

        See `ParameterizedBaseHandler.filter` for more information.

        Parameters:
            keyboard (List[List[Button]]): The inline keyboard you want to
                process.
            callback_query_id (str): The unique identifier of the callback
                for which the keyboard is generated.

        Returns:
            List[List[InlineKeyboardButton]]: The generated keyboard in a
            Pyrogram-compatible type.
        """

        content = {}

        for row in keyboard:
            for button in row:
                content[button.button_id] = {
                    "callback_query_id": str(callback_query_id),
                    **button.parameters,
                }

        self.database.set(callback_query_id, json.dumps(content))

        return [
            [
                InlineKeyboardButton(
                    button.name,
                    " ".join(
                        map(
                            str,
                            [
                                callback_query_id,
                                button.button_id,
                                button.element_id,
                            ],
                        )
                    )
                    .strip()
                    .rstrip(),
                )
                for button in row
            ]
            for row in keyboard
        ]

    def setup(self, client: Client):
        """Make all the defined menus reachable by the client by adding handlers that
        catch all their identifiers to it. It adds support to parameterization
        by applying `ParameterizedBaseHandler.filter` to all the handled
        callback queries. It also calls `pass_handler_and_clean`, which lets
        the callback functions get this handler as argument and deletes
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
            client.add_handler(
                CallbackQueryHandler(
                    pass_handler_and_clean(menu.on_callback, self),
                    self.filter(menu.menu_id),
                )
            )


def pass_handler_and_clean(
    func: Types.Callback, handler: ParameterizedBaseHandler
) -> Types.PyrogramCallback:
    """Generate a function which, whenever it is called, subsequently calls
    `callback`, passing the handler from which this object was generated, and
    then deletes the key which is associated to the handled query from the
    database. It requires a subclass of `ParameterizedBaseHandler` to be
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
            handler.database.delete(context.parameters["callback_query_id"])
        else:
            func(handler, client, context, {})

    return on_callback
