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

from datetime import timedelta
from typing import Any, Callable, Dict, List, Optional, Union

from pyrogram import Client
from pyrogram.types import InputMedia

from pyrubrum.keyboard.element import Element


class Types:
    Callback = Callable[
        ["BaseHandler", Client, Any, Optional[Dict[str, Any]]], None
    ]
    """This type defines the possible values for functions that work as
    callbacks in Pyrubrum (e.g. `on_callback`, `on_message`). They must
    implement the following pattern to be valid::

        callback(handler, client, context, parameters=None)
    """

    Content = Union[
        Union[InputMedia, str],
        Callable[
            ["Handler", Client, Any, Dict[str, Any]], Union[InputMedia, str],
        ],
    ]
    """This type defines the possible values for the content that is provided as
    argument to a menu. A string or an instance of `InputMedia
    <pyrogram.InputMedia>` is suitable for this type to be valid.
    A function that returns such values is valid as well and must follow this
    pattern::

        content(handler, client, context, parameters=None)
    """

    Expire = Optional[Union[bool, int, timedelta]]
    """This type defines the possible values for an expire (see `BaseDatabase`).
    A positive integer is suitable and indicates how many seconds a value can
    be kept within database. A `datetime.timedelta` can be provided and is
    valid as well. In order to indicate that there is no expire, ``False``
    shall be provided.
    """

    Items = Union[
        List[Element],
        Callable[
            ["ParameterizedHandler", Client, Any, Dict[str, Any]],
            List[Element],
        ],
    ]
    """This type defines the possible values for items that are provided as
    argument to `PageMenu`. A list of `Element` is suitable for this type.
    A function that returns such list is valid as well and must follow this
    pattern::


        items(handler, client, context, parameters)
    """

    Link = Union[
        str, Callable[["Handler", Client, Any, Dict[str, Any]], str],
    ]
    """This type defines the possible values for the link that is used to build
    an inline button that redirects to a website. A string is suitable for this
    type to be valid.
    A function that returns such value is valid as well and must follow this
    pattern::

        link(handler, client, context, parameters=None)
    """

    Payload = Union[
        str, Callable[["Handler", Client, Any, Dict[str, Any]], str],
    ]
    """This type defines the possible values for the parameter that is passed
    to the bot using a deep-link. A string is suitable for this type to be
    valid.
    A function that returns such value is valid as well and must follow this
    pattern::

        payload(handler, client, context, parameters=None)
    """

    Preliminary = Optional[
        Union[
            Callable[["Handler", Client, Any, Dict[str, Any]], None],
            List[Callable[["Handler", Client, Any, Dict[str, Any]], None]],
        ]
    ]
    """This type defines the possible values which can be passed for a
    preliminary function. All the provided functions for this type must
    follow this pattern::

        preliminary(handler, client, context, parameters=None)

    A list of such functions can be provided as well for this type to
    be valid.
    """

    PyrogramCallback = Callable[[Client, Any], None]
    """This type describes the pattern of functions which are added to
    a Pyrogram handler, being it::

        callback(client, context)
    """
