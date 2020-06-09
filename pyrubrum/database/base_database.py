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

from abc import ABC
from abc import abstractmethod
from typing import Optional


class BaseDatabase(ABC):
    @abstractmethod
    def get(self, callback_query_id: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def set(self, callback_query_id: str, data: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, callback_query_id: str) -> bool:
        raise NotImplementedError
