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

from .base_database import BaseDatabase
from .errors import DeleteError
from typing import Optional


class DictDatabase(dict, BaseDatabase):
    def get(self, callback_query_id: str) -> Optional[str]:
        return dict.get(self, callback_query_id)

    def set(self, callback_query_id: str, data: str):
        self.update({callback_query_id: data})

    def delete(self, callback_query_id: str):
        try:
            self.pop(callback_query_id)
        except KeyError:
            raise DeleteError
