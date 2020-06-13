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

from dataclasses import dataclass
from itertools import islice
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

from pyrogram import CallbackQuery
from pyrogram import Client
from pyrogram import InlineKeyboardMarkup
from pyrogram import InputMedia
from pyrogram import Message

from pyrubrum.keyboard import Keyboard
from .base_menu import BaseMenu

Content = Union[
    Union[InputMedia, str],
    Callable[
        ["Handler", Client, Union[CallbackQuery, Message], Dict[str, Any]],
        Union[InputMedia, str],
    ],
]

Preliminary = Optional[
    Callable[
        ["Handler", Client, Union[CallbackQuery, Message], Dict[str, Any]],
        None,
    ]
]


@dataclass(eq=False, init=False, repr=True)
class Menu(BaseMenu):
    """Implementation of a menu who has got, by definition, a content to display
    (i.e. what the user will see by accessing it), a limit of buttons displayed
    per row and a custom text displayed for going back to the parent menu, if
    any.

    Attributes:
        back_button_text (Optional[str]): The text which will be displayed
            inside the button that lets the user go back to the parent menu.
            Defaults to "🔙".
        content (Content): What will be displayed whenever a user accesses this
            menu. Both text and media can be provided. A function can be
            provided as well and must follow the following arguments pattern:
                ``func(handler, client, context, parameters)``
        limit (Optional[int]): The limit of buttons per row. Defaults to 2.
        preliminary (Preliminary): A function which is executed each time
            before doing anything else in `on_callback` and `on_message`.
            Defaults to ``None``, which means that no function is going to
            be executed.

    Note:
        This implementation is compatible with a non parameterized handler.
    """

    back_button_text: Optional[str] = "🔙"
    content: Content
    limit: Optional[int] = 2

    def __init__(
        self,
        name: str,
        menu_id: str,
        content: Union[
            Union[InputMedia, str],
            Callable[
                [
                    "Handler",
                    Client,
                    Union[CallbackQuery, Message],
                    Dict[str, Any],
                ],
                Union[InputMedia, str],
            ],
        ],
        back_button_text: Optional[str] = "🔙",
        limit: Optional[int] = 2,
        preliminary: Preliminary = None,
    ):
        """Initialize the object.

        Args:
            name (str): The name you give to the menu, which will be used as
                the text of callback button, if needed. See `BaseMenu` for more
                information.
            menu_id (str): The unique identifier given to the menu, which will
                refer unequivocally to this entity. The hash for this class is
                generated relying on the content of this field. See `BaseMenu`
                for more information.
            content (Content): What will be displayed whenever a user accesses
                this menu. Both text and media can be provided. A function can
                be provided as well and must follow the following arguments
                pattern:
                    ``func(handler, client, context, parameters)``
            back_button_text (Optional[str]): The text which will be displayed
                inside the button that lets the user go back to the parent
                menu. Defaults to "🔙".
            limit (Optional[int]): The limit of buttons per row. Defaults to 2.
            preliminary (Preliminary): A function which is executed each time
                before doing anything else in `on_callback` and `on_message`.
                Defaults to ``None``, which means that no function is going to
                be executed.
        """

        BaseMenu.__init__(self, name, menu_id)
        self.back_button_text = back_button_text
        self.content = content
        self.limit = limit
        self.preliminary = preliminary

    def get_content(
        self,
        handler: "Handler",  # noqa
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Dict[str, Any],
    ) -> Union[InputMedia, str]:
        """Get the content of the menu, if defined. Otherwise call an already provided
        function and returns its value.

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which the
                button is generated.
            parameters (Dict[str, Any]): The parameters which were passed to
                the handler.

        Returns:
            Union[InputMedia, str]: The content of the menu, which is then
                displayed to the user as a media (if it is a subclass of
                `InputMedia`) or a message (if it is just a string).
        """
        if callable(self.content):
            return self.content(handler, client, context, parameters)

        return self.content

    def on_callback(
        self,
        handler: "Handler",  # noqa
        client: Client,
        callback: CallbackQuery,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """Each time a callback query is handled, this function calls the preliminary
        function (i.e. `Menu.preliminary`), if callable, then gets the content
        that is going to be provided to the user (both text and media are
        compatible), sets up an inline keyboard filled with all the references
        to the menus that are linked to the children of this menu node,
        including a special button for going back to the parent menu, whose
        text is defined using `Menu.back_button_text`, which overwrites the
        text of the parent menu which usually should be displayed (see
        `Menu.keyboard`), and finally edits the message with
        `CallbackQuery.edit_message_text` (if the content is a string, i.e. a
        text) or `CallbackQuery.edit_message_media` (if the content is an
        instance of `InputMedia`, i.e. a media).

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (CallbackQuery): The callback query for which the button is
                generated.
            parameters (Dict[str, Any]): The parameters which were passed to
                the handler.
        """
        if not parameters:
            parameters = {}

        if callable(self.preliminary):
            self.preliminary(handler, client, callback, parameters)

        content = self.get_content(handler, client, callback, parameters)

        if isinstance(content, InputMedia):
            callback.edit_message_media(
                content,
                reply_markup=self.keyboard(
                    handler, client, callback, parameters
                ),
            )
        elif isinstance(content, str):
            callback.edit_message_text(
                content,
                reply_markup=self.keyboard(
                    handler, client, callback, parameters
                ),
            )
        else:
            raise TypeError("content must be of type InputMedia or str")

    def on_message(
        self,
        handler: "Handler",  # noqa
        client: Client,
        message: Message,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """Each time a message is handled, this function calls the preliminary
        function (i.e. `Menu.preliminary`), if callable, then gets the content
        that is going to be provided to the user (both text and media are
        compatible), sets up an inline keyboard filled with all the references
        to the menus that are linked to the children of this menu node), and
        finally sends the message with `Message.reply_text` (if the content is
        a string, i.e. a text) or `Message.reply_cached_media` (if the content
        is an instance of `InputMedia`, i.e. a media).

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (Message): The message for which the button is generated.
            parameters (Dict[str, Any]): The parameters which were passed to
                the handler.
        """
        if not parameters:
            parameters = {}

        if callable(self.preliminary):
            self.preliminary(handler, client, message, parameters)

        content = self.get_content(handler, client, message, parameters)

        if isinstance(content, InputMedia):
            message.reply_cached_media(
                file_id=content.media,
                file_ref=content.file_ref,
                caption=content.caption,
                reply_markup=self.keyboard(
                    handler, client, message, parameters
                ),
            )
        elif isinstance(content, str):
            message.reply_text(
                content,
                reply_markup=self.keyboard(
                    handler, client, message, parameters
                ),
            )
        else:
            raise TypeError("content must be of type InputMedia or str")

    def keyboard(
        self,
        handler: "Handler",  # noqa
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Dict[str, Any],
    ) -> InlineKeyboardMarkup:
        """Provide a keyboard, filled with all the buttons which refer to the menus
        that are linked to the children of this menu node and a special button
        for linking the user to the parent menu, if any.

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
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

        if children:
            iterable = iter(children)
            keyboard = list(
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

    def preliminary(
        self,
        handler: "Handler",  # noqa
        client: Client,
        context: Union[CallbackQuery, Message],
        parameters: Dict[str, Any],
    ):
        """Execute some steps before getting the content which is displayed
        inside the menu. It doesn't do anything by default. In order to give
        an actual meaning to this method, you should implement it by yourself
        by creating a subclass.

        Args:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (Union[CallbackQuery, Message]): The context for which the
                button is generated.
            parameters (Dict[str, Any]): The parameters which were passed to
                the handler.
        """
        pass
