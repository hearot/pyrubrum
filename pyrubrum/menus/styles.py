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

from enum import IntFlag


class PageStyle(IntFlag):
    NO_PAGE = 0
    """Do just show the arrows for moving on to the next menu or going
    back to the previous menu.
    """

    HIDE_ON_SINGLE_PAGE = 1
    """Hide the page counter if there is only one page.
    """

    SHOW_PAGE = 2
    """Show the arrows for moving on to the next menu or going back to
    the previous menu with the number of the current page between them.
    """

    SHOW_COUNTER = 4
    """Show the arrows for moving on to the next menu or going back to
    the previous menu with the number of the current page and the number
    of total pages between them.
    """
