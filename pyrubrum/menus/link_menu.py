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

from typing import Any, Dict, Optional

from pyrogram import Client

from pyrubrum.keyboard.button import Button
from pyrubrum.types import Types

from .base_menu import BaseMenu


class LinkMenu(BaseMenu):
    """Implementation of a menu which represents a link to a website.

    Parameters:
        name (str): The name you give to the menu, which will be used as
            the text of callback button, if needed. See `BaseMenu` for more
            information.
        menu_id (str): The unique identifier given to the menu, which will
            refer unequivocally to this entity. The hash for this class is
            generated relying on the content of this field. Avoid using ``0``
            as it is used for buttons whose purpose is only related to
            design (i.e. they do not point to any menu, see
            :term:`Null-pointer button`). See `BaseMenu` for more information.
        link (Types.Content): What will be displayed whenever a user
            accesses this menu. A function can be provided as well and must
            follow the following arguments pattern::

                func(handler, client, context, parameters)

    """

    def __init__(self, name: str, menu_id: str, link: Types.Link):
        BaseMenu.__init__(self, name, menu_id, is_link=True)

        self.link = link

    def button(
        self,
        handler: "BaseHandler",  # noqa
        client: "Client",  # noqa
        context: Any,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Button:
        """Create an inline button which redirects to a website retrieved from
        `LinkMenu.link`, using `name` as the content of the text field.

        Parameters:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which
                button is generated for.
            parameters (Optional[Dict[str, Any]]): The parameters which were
                passed to the handler. Defaults to ``None``.

        Returns:
            Button: The generated button.
        """
        if callable(self.link):
            return Button(
                self.name,
                self.menu_id,
                link=self.link(handler, client, context, parameters),
            )

        return Button(self.name, self.menu_id, link=self.link)
