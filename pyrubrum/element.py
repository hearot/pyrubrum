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


@dataclass
class Element:
    """Representation of a general flag which refers to a particular state of a
    menu. It can be passed as an argument to `Button`.

    Attributes:
        name (str): The text which will be displayed in the text field of a
            button inside an inline keyboard.
        element_id (str): The unique identifier for this object which makes a
            menu recognise it.
    """

    name: str
    element_id: str
