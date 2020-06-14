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

from itertools import islice
from math import ceil
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from pyrogram import CallbackQuery
from pyrogram import Client
from pyrogram import InlineKeyboardMarkup
from pyrogram import InputMedia
from pyrogram import Message
from pyrogram.client.filters.filters import Filter

from pyrubrum.keyboard import Button
from pyrubrum.keyboard import Keyboard
from pyrubrum.types import Types
from .menu import Menu
from .styles import PageStyle


class PageMenu(Menu):
    """Implementation of a menu which automatically, given a list of items, manages
    paging and the setting of parameters. It has got, by definition, a list of
    items, which can be provided using a custom function as well, a limit of
    displayed elements per page and custom texts for the buttons which let the
    user change the displayed page.

    Parameters:
        name (str): The name you give to the menu, which will be used as
            the text of callback button, if needed. See `BaseMenu` for more
            information.
        menu_id (str): The unique identifier given to the menu, which will
            refer unequivocally to this entity. The hash for this class is
            generated relying on the content of this field. Avoid using ``0``
            as it is used for buttons whose purpose is only related to design
            (i.e. they do not point to any menu). See `BaseMenu` for more
            information.
        content (Types.Content): What will be displayed whenever a user
            accesses this menu. Both text and media can be provided. A
            function can be provided as well and must follow the following
            arguments pattern::

                func(handler, client, context, parameters)

            See `Menu` for more information.
        items (types.Items): The list of elements the menu is compounded of or
            a function which returns such type of value.
        back_button_text (Optional[str]): The text which will be displayed
            inside the button that lets the user go back to the parent
            menu. Defaults to "🔙". See `Menu` for more information.
        default (Optional[bool]): If this menu shall be displayed if no
            other top-level menu has been matched. It works only if this
            menu is a top-level one.
        limit (Optional[int]): The limit of buttons per row. Defaults to 2.
            See `Menu` for more information.
        limit_page (Optional[int]): The limit of elements per page.
            Defaults to 4.
        message_filter (Optional[Filter]): A filter for telling Pyrogram
            when a message should be associated to this menu. It works only
            for top-level menus (see `Handler.setup`). Defaults to ``None``,
            which automatically makes this menu reachable when the user texts
            a message that follows this pattern::

                /[MENU_ID]

        next_page_button_text (Optional[str]): The text which is displayed
            inside the button that lets the user move on to the next page,
            if any. Defaults to "▶️".
        page_style (Optional[int]): The chosen style for displaying the page.
            See `PageStyle`. Defaults to
            `PageStyle.SHOW_PAGE | PageStyle.HIDE_ON_SINGLE_PAGE`.
        preliminary (Types.Preliminary): A function which is executed each time
            before doing anything else in `on_callback` and `on_message`.
            You can provide a list of such functions as well, which will be
            executed following the same order as the one of the list.
            Defaults to ``None``, which means that no function is going to
            be executed.
        previous_page_button_text (Optional[str]): The text which is
            displayed inside the button that lets the user go back to the
            previous page, if any. Defaults to "◀️".

    Warning:
        This implementation is not compatible with a non-parameterized handler.
        An handler that supports parameterization is required.
    """

    def __init__(
        self,
        name: str,
        menu_id: str,
        content: Union[InputMedia, str],
        items: Types.Items,
        back_button_text: Optional[str] = "🔙",
        default: Optional[bool] = False,
        limit: Optional[int] = 2,
        limit_page: Optional[int] = 4,
        message_filter: Optional[Filter] = None,
        next_page_button_text: Optional[str] = "▶️",
        page_style: Optional[int] = PageStyle.SHOW_PAGE
        | PageStyle.HIDE_ON_SINGLE_PAGE,
        preliminary: Types.Preliminary = None,
        previous_page_button_text: Optional[str] = "◀️",
    ):
        Menu.__init__(
            self,
            name,
            menu_id,
            content,
            back_button_text=back_button_text,
            default=default,
            limit=limit,
            message_filter=message_filter,
            preliminary=preliminary,
        )

        self.items = items
        self.limit_page = limit_page
        self.next_page_button_text = next_page_button_text
        self.page_style = page_style
        self.previous_page_button_text = previous_page_button_text

    def keyboard(
        self,
        handler: "ParameterizedHandler",  # noqa
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Dict[str, Any],
    ) -> InlineKeyboardMarkup:
        """Provide a keyboard which is created relying on the page provided by the
        parameters and is built following the limits defined during the
        initialization of this instance (i.e. `limit` and `limit_page`).

        The page is retrieved from the parameters relying on the page
        identifier, which is built in the following way::

            page_[MENU_ID]

        Hence, there is a special set of keys for parameters that is
        recommended not to be used in order to handle paging in a proper way.
        All keys starting with ``page_`` shall then be avoided.

        If this menu has been referenced by this menu itself (i.e. the user
        clicked on the buttons for moving between pages), the page is set to be
        equal to ``element_id``, which represents the page itself.

        As a result of this, during the build of the the teleport buttons (i.e.
        the buttons for moving between pages) the ``element_id`` is set to be
        equal to the page the buttons refer to (e.g. page plus one for "Go to
        the next page").

        In the end, the keyboard is filled with all the buttons which refer to
        the menus that are linked to the children of this menu node and a
        special button for linking the user to the parent menu, if any.

        Parameters:
            handler (ParameterizedHandler): The handler which coordinates the
                management of the menus and supports parameterization.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which the
                button is generated.
            parameters (Dict[str, Any]): The parameters which were passed to
                the handler.

        Returns:
            InlineKeyboardMarkup: The generated inline keyboard, which is then
            displayed to the user.
        """
        parent, children = handler.get_family(self.menu_id)

        keyboard = []
        items = []
        page_id = "page_" + self.menu_id

        if page_id not in parameters:
            parameters[page_id] = 0

        if "same_menu" in parameters and parameters["same_menu"]:
            parameters[page_id] = int(parameters["element_id"])

        if children:
            iterable = iter(children)
            page_item_menu = next(iterable)

            if callable(self.items):
                items = self.items(handler, client, context, parameters)
            elif isinstance(self.items, list):
                items = self.items
            else:
                raise TypeError("items must be either callable or a list")

            elements = items[parameters[page_id] * self.limit_page :][
                : self.limit_page
            ]

            keyboard = [
                [
                    Button(
                        element.name,
                        page_item_menu.menu_id,
                        parameters,
                        element.element_id,
                    )
                    for element in elements[i : i + self.limit]
                ]
                for i in range(0, len(elements), self.limit)
            ]

        if children:
            keyboard += list(
                iter(
                    lambda: list(
                        map(
                            lambda child: child.button(
                                handler, client, context, parameters
                            ),
                            islice(iterable, self.limit),
                        )
                    ),
                    [],
                )
            )

        teleport_row = []
        pages = ceil(len(items) / self.limit_page)

        if parameters[page_id] > 0:
            previous_page_button = Button(
                self.previous_page_button_text,
                self.menu_id,
                parameters,
                parameters[page_id] - 1,
                True,
            )

            if self.menu_id + "_id" in parameters:
                previous_page_button.parameters[
                    self.menu_id + "_id"
                ] = parameters[self.menu_id + "_id"]

            teleport_row.append(previous_page_button)

        if self.page_style != PageStyle.NO_PAGE and (
            self.page_style % 2 != 1 or not pages <= 1
        ):
            if self.page_style >= PageStyle.SHOW_COUNTER:
                page_button = Button(
                    "%d/%d" % (parameters[page_id] + 1, pages),
                    str(parameters[page_id]),
                    "0",
                )

                teleport_row.append(page_button)
            else:
                page_button = Button(str(parameters[page_id] + 1), "0")

                teleport_row.append(page_button)

        if (parameters[page_id] + 1) * self.limit_page < len(items):
            next_page_button = Button(
                self.next_page_button_text,
                self.menu_id,
                parameters,
                parameters[page_id] + 1,
                True,
            )

            if self.menu_id + "_id" in parameters:
                next_page_button.parameters[self.menu_id + "_id"] = parameters[
                    self.menu_id + "_id"
                ]

            teleport_row.append(next_page_button)

        if teleport_row:
            keyboard += [teleport_row]

        if parent:
            parent_button = parent.button(handler, client, context, parameters)
            parent_button.name = self.back_button_text

            keyboard = keyboard + [[parent_button]]

        if isinstance(context, Message):
            return (
                Keyboard(
                    keyboard,
                    handler,
                    str(context.message_id) + str(context.from_user.id),
                )
                if keyboard
                else None
            )
        elif isinstance(context, CallbackQuery):
            return (
                Keyboard(keyboard, handler, context.id) if keyboard else None
            )
