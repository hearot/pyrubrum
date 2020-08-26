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

from abc import ABC
from typing import Any, Dict, Optional

from pyrogram import Client

from pyrubrum.handlers import BaseHandler
from pyrubrum.keyboard import Button


class BaseMenu(ABC):
    """Basic represention of a menu, which is an entity that has got by definition
    at least a name, a unique identifier and an associated button, which can
    be arbitrarily generated.

    A menu can represent a link as well (see `BaseMenu.is_link`), although it
    doesn't by default.

    The purpose of this class is to give a general interface for a menu, as it
    doesn't implement anything except for the generation of both buttons and
    hashes.

    See Also:
        For complete implementations of this class:

        * `LinkMenu`
        * `Menu`
        * `PageMenu`

    Parameters:
        name (str): The name you give to the menu, which will be used as the
            text of callback button, if needed.
        menu_id (str): The unique identifier given to the menu, which will
            refer unequivocally to this entity. The hash for this class is
            generated relying on the content of this field. Avoid using ``0``
            as it is used for buttons whose purpose is only related to design
            (i.e. they do not point to any menu, see :term:`Null-pointer
            button`).
        is_link (Optional[bool]): If this menu represents a link.

    Warning:
        Avoid using the same identifier for other entities, as it will result
        in ambiguity.
    """

    def __hash__(self) -> int:
        """The hash generator of a menu, relying on the unique identifier
        (`menu_id`) which is assigned to it.

        Returns:
            int: The unique hash which is generated for this entity.
        """
        return hash(self.menu_id)

    def __init__(
        self, name: str, menu_id: str, is_link: Optional[bool] = False
    ):
        self.is_link = is_link
        self.name = name
        self.menu_id = menu_id

    def button(
        self,
        handler: BaseHandler,
        client: Client,
        context: Any,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Button:
        """Create an inline button which refers to this menu, using `name` as
        the content of the text field and `menu_id` as the unique identifier
        of the `Button` object.

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
        return Button(self.name, self.menu_id, parameters)
