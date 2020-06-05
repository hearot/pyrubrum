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

from .base_database import BaseDatabase
from .errors import DeleteError, ExpireError, SetError
from datetime import timedelta
from typing import Optional, Union
import redis # noqa


class RedisDatabase(BaseDatabase):
    encoding = 'utf-8'
    expire: Optional[Union[int, timedelta]] = 86400
    server: redis.Redis

    def __init__(self, server: redis.Redis,
                 encoding='utf-8',
                 expire: Optional[Union[int, timedelta]] = 86400):
        self.encoding = encoding
        self.expire = expire
        self.server = server

    def get(self, callback_query_id: str) -> Optional[str]:
        content = self.server.get(callback_query_id)
        return content.decode(self.encoding) if content else None

    def set(self, callback_query_id: str, data: str):
        if not self.server.set(callback_query_id, data):
            raise SetError

        if self.expire and not self.server.expire(callback_query_id,
                                                  self.expire):
            raise ExpireError

    def delete(self, callback_query_id: str):
        try:
            self.server.delete(callback_query_id)
        except redis.RedisError:
            raise DeleteError
