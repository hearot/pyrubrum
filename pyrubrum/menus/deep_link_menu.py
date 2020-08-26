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

DEEP_LINK_TEMPLATE = "https://t.me/{username}?{deep_link_type}={payload}"
PERMITTED_TYPES = {"start", "startgroup"}
USERNAMES = {}


class DeepLinkMenu(BaseMenu):
    """Implementation of a menu which automatically creates a deep-link,
    given a parameter that shall be passed.

    See also:
        `What the Bot API documentation says about deep-linking.
        <https://core.telegram.org/bots#deep-linking>`_

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
        payload (Types.Payload): What will be passed to as payload using the
            deep-linking. A function can be provided as well and must follow
            the following arguments pattern::

                func(handler, client, context, parameters)
        deep_link_type (Optional[str]): The type of deep-link that is being
            generated, which must be either ``start`` or ``startgroup``.
            Defaults to ``start``.
    """

    def __init__(
        self,
        name: str,
        menu_id: str,
        payload: Types.Payload,
        deep_link_type: Optional[str] = "start",
    ):
        if deep_link_type not in PERMITTED_TYPES:
            raise ValueError(
                "deep_link_type must be either " "'start' or 'startgroup'"
            )

        BaseMenu.__init__(self, name, menu_id, is_link=True)

        self.payload = payload
        self.deep_link_type = deep_link_type

    def button(
        self,
        handler: "BaseHandler",  # noqa
        client: "Client",  # noqa
        context: Any,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Button:
        """Create an inline button which makes use of deep-linking, following
        the defined `DeepLinkMenu.deep_link_type` and passing the parameter
        retrieved from `DeepLinkMenu.payload`.

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
        client_hash = hash(client)

        if client_hash in USERNAMES:
            username = USERNAMES[client_hash]
        else:
            username = client.get_me().username
            USERNAMES[client_hash] = username

        if callable(self.payload):
            return Button(
                self.name,
                self.menu_id,
                link=DEEP_LINK_TEMPLATE.format(
                    deep_link_type=self.deep_link_type,
                    payload=self.payload(handler, client, context, parameters),
                    username=username,
                ),
            )

        return Button(
            self.name,
            self.menu_id,
            link=DEEP_LINK_TEMPLATE.format(
                deep_link_type=self.deep_link_type,
                payload=self.payload,
                username=username,
            ),
        )
