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

from copy import deepcopy
from typing import Any, Dict, Optional


class Button:
    """Representation of a button which belongs to an inline keyboard and has got,
    by definition, a unique identifier, which actually represents the menu this
    object is referring to, an `Element` identifier (i.e. the identifier of the
    object that is carried by the button and is then passed to the menu it is
    referring to, if any), a name, which is displayed inside the text field of
    the inline button, and a dictionary of parameters.

    The dictionary that is passed as argument for representing parameters is
    always deep copied, if not ``None``.

    Parameters:
        name (str): The name which is displayed inside the text field of
            the inline button this object will be converted to.
        menu_id (str): The unique identifier of the button, which is the
            same as the one of the menu the button is referring to.
        parameters (Optional[Dict[str, Any]]): The parameters that will be
            passed to the menu this button is referring to. Defaults to
            ``None`` (i.e. the handler does not support parameterization).
        element_id (Optional[str]): The unique identifier of the `Element`
            the button is carrying, if any. Defaults to an empty string.
        link (Optional[str]): The website this button is referring to, if any.
            If provided, all the other arguments are ignored and this button
            is set to represent a button which redirects to a certain URL,
            which is the provided string itself.
        same_menu (Optional[bool]): If the button is referring to the same
            menu by which it was initialized. Defaults to ``False``.
        **kwargs: Arbitrary keyword arguments which can be used as a way to
            define a new parameter (``key=value``) that will be added to
            the dictionary of parameters.

    Warning:
        There is a special group of names which are not available for being
        used as keys for parameters (not for arguments!). These are
        ``from_chat_id``, ``menu_id``, ``element_id`` and ``same_menu``.
        If provided, they will be overwritten. Keys starting with ``page_``
        should be avoided according to `PageStyle.generate_page_id`.
    """

    def __init__(
        self,
        name: str,
        menu_id: str,
        parameters: Optional[Dict[str, Any]] = None,
        element_id: Optional[str] = "",
        link: Optional[str] = None,
        same_menu: Optional[bool] = False,
        **kwargs
    ):
        self.name = name
        self.link = link

        if link:
            return

        self.menu_id = menu_id
        self.element_id = element_id
        self.same_menu = same_menu

        if isinstance(parameters, dict):
            self.parameters = deepcopy(parameters)
            self.parameters.update(kwargs)
        else:
            self.parameters = None
