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
from typing import Any
from typing import Optional
from typing import Dict


@dataclass(init=False)
class Button:
    """Representation of a button which belongs to an inline keyboard and has got,
    by definition, a unique identifier, which actually represents the menu this
    object is referring to, an `Element` identifier (i.e. the identifier of the
    object that is carried by the button and is then passed to the menu it is
    referring to, if any), a name, which is displayed inside the text field of
    the inline button, and a dictionary of parameters.

    Attributes:
        button_id (str): The unique identifier of the button, which is the same
            as the one of the menu the button is referring to.
        element_id (str): The unique identifier of the `Element` the button is
            carrying, if any. Defaults to an empty string.
        name (str): The name which is displayed inside the text field of the
            inline button this object will be converted to.
        parameters (Dict[str, Any]): The parameters that will be passed to the
            menu this button is referring to.

    Warning:
        There is a special group of names which are not available for being
        used as keys for parameters. These are ``button_id``,
        ``callback_query_id`` and ``same_menu``. If provided, they will be
        overwritten. As a result of being passed as parameter inside a
        callback query (see `ParameterizedBaseHandler.process_keyboard`),
        ``element_id`` does not maintain its type and will always be
        initialized as a string. Keys starting with ``page_`` shall be
        avoided accordingly to `PageMenu.keyboard.
    """

    button_id: str
    element_id: Optional[str] = ""
    name: str
    parameters: Dict[str, Any]

    def __init__(
        self,
        name: str,
        button_id: str,
        parameters: Dict[str, Any],
        element_id: Optional[str] = "",
        same_menu: Optional[bool] = False,
        **kwargs
    ):
        """Initialize the button by setting the attributes of this object and copying
        the dictionary of parameters.

        Args:
            name (str): The name which is displayed inside the text field of
                the inline button this object will be converted to.
            button_id (str): The unique identifier of the button, which is the
                same as the one of the menu the button is referring to.
            parameters (Dict[str, Any]): The parameters that will be passed to
                the menu this button is referring to.
            element_id (Optional[str]): The unique identifier of the `Element`
                the button is carrying, if any. Defaults to an empty string.
            same_menu (Optional[bool]): If the button is referring to the same
                menu by which it was initialized. Defaults to False.
            **kwargs: Arbitrary keyword arguments which can be used as a way to
                define a new parameter (``key=value``) that will be added to
                the dictionary of parameters.
        """

        self.button_id = button_id
        self.element_id = element_id
        self.name = name
        self.parameters = parameters.copy()
        self.parameters.update(kwargs)

        self.parameters["button_id"] = button_id
        self.parameters["same_menu"] = same_menu
