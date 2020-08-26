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

from itertools import islice
from math import ceil
from typing import Any, Dict, List, Optional

from pyrogram import Client

from pyrubrum.handlers.base_handler import NULL_POINTER
from pyrubrum.keyboard.button import Button

from .base_style import BaseStyle

EMPTY_CHARACTER = "‎"


class PageStyle(BaseStyle):
    """Integrate paging into your menu in a simple way by using this
    class.

    Parameters:
        back_text (Optional[str]): The text which will be displayed
            inside the button that lets the user go back to the parent
            menu. Defaults to "🔙".
        limit (Optional[int]): The limit of buttons per row. Defaults to ``2``.
        limit_items (Optional[int]): The limit of elements per page.
            Defaults to ``4``.
        next_page_text (Optional[str]): The text which is displayed
            inside the button that lets the user move on to the next page,
            if any. Defaults to "▶️".
        previous_page_text (Optional[str]): The text which is
            displayed inside the button that lets the user go back to the
            previous page, if any. Defaults to "◀️".
        show_counter (Optional[bool]): If there shall be the number of the
            total pages right next to the number of page. Defaults to
            ``True``.
        show_page (Optional[bool]): If the number of the page shall be
            displayed between the two arrows for managing the motion of
            the pages. Defaults to ``True``.

    Warning:
        This implementation is not compatible with a non-parameterized handler.
        An handler that supports parameterization is required.
    """

    def __init__(
        self,
        back_text: Optional[str] = "🔙",
        limit: Optional[int] = 2,
        limit_items: Optional[int] = 4,
        next_page_text: Optional[str] = "▶️",
        previous_page_text: Optional[str] = "◀️",
        show_counter: Optional[bool] = True,
        show_page: Optional[bool] = True,
    ):
        self.back_text = back_text
        self.limit = limit
        self.limit_items = limit_items
        self.next_page_text = next_page_text
        self.previous_page_text = previous_page_text
        self.show_counter = show_counter
        self.show_page = show_page

    def generate_page_id(
        self,
        handler: "ParameterizedHandler",  # noqa
        client: Client,
        context: Any,
        parameters: Dict[str, Any],
        menu: "PageMenu",  # noqa
    ) -> str:
        """Generate a page identifier, relying on the identifier of the provided menu,
        built in the following way::

            page_[MENU_ID]

        Hence, there is a special set of keys for parameters that is
        recommended not to be used in order to handle paging in a proper way.
        All keys starting with ``page_`` shall then be avoided.

        Parameters:
            handler (ParameterizedHandler): The handler which coordinates the
                management of the menus and supports parameterization.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which the
                button is generated.
            parameters (Dict[str, Any]): The parameters which were passed to
                the handler.
            menu (Menu): The menu the keyboard is being built for.

        Returns:
            str: The generated page identifier.
        """
        page_id = "page_" + menu.menu_id

        if page_id not in parameters:
            parameters[page_id] = 0

        if "same_menu" in parameters and parameters["same_menu"]:
            parameters[page_id] = int(parameters["element_id"])

        return page_id

    def generate(
        self,
        handler: "ParameterizedHandler",  # noqa
        client: Client,
        context: Any,
        parameters: Dict[str, Any],
        menu: "Menu",  # noqa
    ) -> List[List["Button"]]:
        """Provide a keyboard which is created relying on the page provided by the
        parameters and is built following the limits defined during the
        initialization of this instance (i.e. `limit` and `limit_items`).

        The page identifier is retrieved from `PageStyle.generate_page_id`.

        If this menu has been referenced by this menu itself (i.e. the user
        clicked on the buttons for moving between pages), the page is set to be
        equal to ``element_id``, which represents the page itself.

        As a result of this, during the build of the the teleport buttons (i.e.
        the buttons for moving between pages) ``element_id`` is set to be
        equal to the page the buttons refer to (e.g. page plus one for "Go to
        the next page").

        No teleport keyboard is generated if the number of total pages is equal
        to one. Otherwise, three buttons are generated. The first one is built
        in order to let the user go back to the previous page, if any, else a
        :term:`null-pointer button <Null-pointer button>` is created, with its
        content being an empty character. The second one is generated if and
        only if `PageStyle.show_menu` is set to be ``True``, with its text
        being the current number of page (concatenated to the number of total
        pages if `PageStyle.show_counter` is set to be ``True``). The third
        one is designed for moving on to the next page, if any, and it is built
        following the same rules that were respected by the first button.

        In the end, the keyboard is filled with all the buttons which refer to
        the children menus a special button for linking the user to the parent
        menu, if any.

        Parameters:
            handler (ParameterizedHandler): The handler which coordinates the
                management of the menus and supports parameterization.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which the
                button is generated.
            parameters (Dict[str, Any]): The parameters which were passed to
                the handler.
            menu (Menu): The menu the keyboard is being built for.

        Returns:
            List[List[Button]]: The generated inline keyboard, which is then
            displayed to the user.
        """
        page_id = self.generate_page_id(
            handler, client, context, parameters, menu
        )

        parent, children = handler.get_family(menu.menu_id)

        keyboard = []

        if children:
            iterable = iter(children)
            page_item_menu = next(iterable)

            if callable(menu.items):
                items = menu.items(handler, client, context, parameters)
            elif isinstance(menu.items, list):
                items = menu.items
            else:
                raise TypeError("items must be either callable or a list")

            elements = items[parameters[page_id] * self.limit_items :][
                : self.limit_items
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

        pages = ceil(len(items) / self.limit_items)

        if pages > 1:
            teleport_row = []

            if parameters[page_id] > 0:
                previous_page_button = Button(
                    self.previous_page_text,
                    menu.menu_id,
                    parameters,
                    element_id=parameters[page_id] - 1,
                    same_menu=True,
                )

                if menu.menu_id + "_id" in parameters:
                    previous_page_button.parameters[
                        menu.menu_id + "_id"
                    ] = parameters[menu.menu_id + "_id"]

                teleport_row.append(previous_page_button)
            else:
                previous_page_button = Button(
                    EMPTY_CHARACTER, str(parameters[page_id]), NULL_POINTER,
                )

                teleport_row.append(previous_page_button)

            if self.show_page:
                if self.show_counter:
                    page_button = Button(
                        "%d/%d" % (parameters[page_id] + 1, pages),
                        str(parameters[page_id]),
                        NULL_POINTER,
                    )

                    teleport_row.append(page_button)
                else:
                    page_button = Button(
                        str(parameters[page_id] + 1), NULL_POINTER
                    )

                    teleport_row.append(page_button)

            if parameters[page_id] + 1 < pages:
                next_page_button = Button(
                    self.next_page_text,
                    menu.menu_id,
                    parameters,
                    element_id=parameters[page_id] + 1,
                    same_menu=True,
                )

                if menu.menu_id + "_id" in parameters:
                    next_page_button.parameters[
                        menu.menu_id + "_id"
                    ] = parameters[menu.menu_id + "_id"]

                teleport_row.append(next_page_button)
            else:
                next_page_button = Button(
                    EMPTY_CHARACTER, str(parameters[page_id]), NULL_POINTER,
                )

                teleport_row.append(next_page_button)

            keyboard += [teleport_row]

        if parent:
            parent_button = parent.button(handler, client, context, parameters)
            parent_button.name = self.back_text

            keyboard += [[parent_button]]

        return keyboard
