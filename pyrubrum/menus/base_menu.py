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
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from pyrogram import CallbackQuery
from pyrogram import Client
from pyrogram import InlineKeyboardMarkup
from pyrogram import InputMedia
from pyrogram import Message

from pyrubrum.handlers import BaseHandler
from pyrubrum.keyboard import Button


@dataclass(eq=False, init=False, repr=True)
class BaseMenu(ABC):
    """Basic represention of a menu, which is an entity that has got by definition
    at least a name and a unique identifier.

    The purpose of this class is to give a general interface for a menu, as it
    doesn't implement anything except for the generation of both buttons and
    hashes.

    A sample implementation of this interface is `Menu`.

    Attributes:
        name (str): The name you give to the menu, which will be used as the
            text of callback button, if needed.
        menu_id (str): The unique identifier given to the menu, which will
            refer unequivocally to this entity. The hash for this class is
            generated relying on the content of this field.

    Note:
        In order to create a subclass or to access this interface, you will
        need to implement all the defined abstract methods, which are
        `get_content`, `keyboard, `on_callback`, `on_message`. Otherwise, you
        will get an error.

    Warning:
        Avoid using the same identifier for other entities, as it will result
        in ambiguity.
    """

    name: str
    menu_id: str

    def __hash__(self) -> int:
        """The hash generator of a menu, relying on the unique identifier
        (`menu_id`) which is assigned to it.

        Returns:
            int: The unique hash which is generated for this entity.
        """
        return hash(self.menu_id)

    def __init__(self, name: str, menu_id: str):
        """Initialize the class with a custom name and unique identifier.

        Args:
            name (str): The name you give to the menu, which will be used as
                the text of callback button, if needed.
            menu_id (str): The unique identifier given to the menu, which will
                refer unequivocally to this entity. The hash for this class is
                generated relying on the content of this field.
        """
        self.name = name
        self.menu_id = menu_id

    def button(
        self,
        handler: BaseHandler,
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Button:
        """Create an inline button which refers to this menu, using `name` as
        the content of the text field and `menu_id` as the unique identifier
        of the `Button` object.

        Args:
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

    @abstractmethod
    def get_content(
        self,
        handler: BaseHandler,
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Union[InputMedia, str]:
        """This abstract method is intended to be implemented as a generator
        for the content of the menu (i.e. what the user will see after clicking
        on the inline button or referencing to the menu using a bot command).

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which the
                button is generated.
            parameters (Optional[Dict[str, Any]]): The parameters which were
                passed to the handler. Defaults to ``None``.

        Returns:
            Union[InputMedia, str]: The content of the menu, which is then
                displayed to the user as a media (if it is a subclass of
                `InputMedia`) or a message (if it is just a string).
        """
        raise NotImplementedError

    @abstractmethod
    def keyboard(
        self,
        handler: BaseHandler,
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> InlineKeyboardMarkup:
        """This abstract method is intended to be implemented as a generator
        for the keyboard of the menu (aka the inline keyboard).

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which the
                button is generated.
            parameters (Optional[Dict[str, Any]]): The parameters which were
                passed to the handler. Defaults to ``None``.

        Returns:
            InlineKeyboardMarkup: The generated inline keyboard, which is then
                displayed to the user.
        """
        raise NotImplementedError

    @abstractmethod
    def on_callback(
        self,
        handler: BaseHandler,
        client: Client,
        callback: CallbackQuery,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """This abstract method is intended to be implemented and is called
        whenever a callback query is handled and refers to this menu.

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            callback (CallbackQuery): The callback query for which the button
                is generated.
            parameters (Optional[Dict[str, Any]]): The parameters which were
                passed to to the handler. Defaults to ``None``.
        """
        raise NotImplementedError

    @abstractmethod
    def on_message(
        self,
        handler: BaseHandler,
        client: Client,
        message: Message,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """This abstract method is intended to be implemented and is called
        whenever a message is handled and refers to this menu.

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            message (Message): The message for which the button is generated.
            parameters (Optional[Dict[str, Any]]): The parameters which were
                passed to to the handler. Defaults to ``None``.
        """
        raise NotImplementedError
