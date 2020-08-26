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
from typing import Any, Dict, List

from pyrogram import Client


class BaseStyle(ABC):
    """Basic representation of a style that can be used in order to
    create a keyboard for `Menu.keyboard`.
    """

    @abstractmethod
    def generate(
        self,
        handler: "Handler",  # noqa
        client: Client,
        context: Any,
        parameters: Dict[str, Any],
        menu: "Menu",  # noqa
    ) -> List[List["Button"]]:
        """This abstract method is intended to be implemented as a keyboard
        generator.

        Parameters:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which the
                button is generated.
            parameters (Dict[str, Any]): The parameters which were passed to
                the handler.
            menu (Menu): The menu the keyboard is being built for.

        Returns:
            pyrogram.InlineKeyboardMarkup: The generated inline keyboard,
            which is then displayed to the user.
        """
        raise NotImplementedError
