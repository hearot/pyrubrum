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

import pytest

from pyrubrum import DictDatabase
from pyrubrum import NotFoundError

database = DictDatabase()


def test_set():
    database.set("A", "B")

    assert "A" in database
    assert database["A"] == "B"


def test_get():
    assert database.get("A") == "B"

    with pytest.raises(NotFoundError):
        database.get("C")


def test_delete():
    database.delete("A")
    assert "A" not in database

    with pytest.raises(NotFoundError):
        database.delete("A")
