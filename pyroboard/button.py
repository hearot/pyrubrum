# Pyroboard - Keyboard manager for Pyrogram
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyroboard.
#
# Pyroboard is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyroboard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyroboard. If not, see <http://www.gnu.org/licenses/>.

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(init=False)
class Button:
    button_id: str
    element_id: str = ""
    name: str
    parameters: dict

    def __init__(self, name: str, button_id: str,
                 parameters: Dict[str, Any],
                 element_id: str = "",
                 same_menu: bool = False,
                 **kwargs):
        self.button_id = button_id
        self.element_id = element_id
        self.name = name
        self.parameters = parameters.copy()
        self.parameters.update(kwargs)

        self.parameters['button_id'] = button_id
        self.parameters['same_menu'] = same_menu
