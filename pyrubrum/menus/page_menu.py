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

from typing import Optional
from typing import Union

from pyrogram import InputMedia
from pyrogram.client.filters.filters import Filter

from pyrubrum.menus.styles import BaseStyle
from pyrubrum.menus.styles import PageStyle
from pyrubrum.types import Types
from .menu import Menu


class PageMenu(Menu):
    """Implementation of a menu which automatically, given a list of items, manages
    paging and the setting of parameters. It has got, by definition, a list of
    items, which can be provided using a custom function as well, a limit of
    displayed elements per page and custom texts for the buttons which let the
    user change the displayed page.

    See Also:
        For understanding how the keyboard is being generated:

        * `PageStyle`

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
        default (Optional[bool]): If this menu shall be displayed if no
            other top-level menu has been matched. It works only if this
            menu is a top-level one.
        message_filter (Optional[Filter]): A filter for telling Pyrogram
            when a message should be associated to this menu. It works only
            for top-level menus (see `Handler.setup`). Defaults to ``None``,
            which automatically makes this menu reachable when the user texts
            a message that follows this pattern::

                /[MENU_ID]

        preliminary (Types.Preliminary): A function which is executed each time
            before doing anything else in `on_callback` and `on_message`.
            You can provide a list of such functions as well, which will be
            executed following the same order as the one of the list.
            Defaults to ``None``, which means that no function is going to
            be executed.
        style (BaseStyle): The class which generates the keyboard for this
            function following a certain style. Defaults to `PageStyle()`.

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
        default: Optional[bool] = False,
        message_filter: Optional[Filter] = None,
        preliminary: Types.Preliminary = None,
        style: BaseStyle = PageStyle(),
    ):
        """Roughly equivalent to::

            Menu(self, name, menu_id, content, default, message_filter,
                 preliminary, style, items=items)
        """
        Menu.__init__(
            self,
            name,
            menu_id,
            content,
            default=default,
            message_filter=message_filter,
            preliminary=preliminary,
            style=style,
        )

        self.items = items
