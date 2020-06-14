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

from datetime import timedelta
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import List
from typing import Union

from pyrogram import CallbackQuery
from pyrogram import Client
from pyrogram import InputMedia
from pyrogram import Message

from pyrubrum.keyboard.element import Element


class Types:
    Callback = Union[
        Callable[["BaseHandler", Client, CallbackQuery], None],
        Callable[["BaseHandler", Client, Message], None],
    ]

    Content = Union[
        Union[InputMedia, str],
        Callable[
            ["Handler", Client, Union[CallbackQuery, Message], Dict[str, Any]],
            Union[InputMedia, str],
        ],
    ]

    Expire = Optional[Union[bool, int, timedelta]]

    Items = Union[
        List[Element],
        Callable[
            [
                "ParameterizedHandler",
                Client,
                Union[CallbackQuery, Message],
                Dict[str, Any],
            ],
            List[Element],
        ],
    ]

    Preliminary = Optional[
        Union[
            Callable[
                [
                    "Handler",
                    Client,
                    Union[CallbackQuery, Message],
                    Dict[str, Any],
                ],
                None,
            ],
            List[
                Callable[
                    [
                        "Handler",
                        Client,
                        Union[CallbackQuery, Message],
                        Dict[str, Any],
                    ],
                    None,
                ]
            ],
        ]
    ]

    PyrogramCallback = Union[
        Callable[[Client, CallbackQuery], None],
        Callable[[Client, Message], None],
    ]
