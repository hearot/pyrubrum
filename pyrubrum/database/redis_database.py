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

from datetime import timedelta
from typing import Optional
from typing import Union

from .base_database import BaseDatabase
from .errors import DeleteError
from .errors import ExpireError
from .errors import SetError

try:
    import redis
except (ImportError, ModuleNotFoundError):
    pass


class RedisDatabase(BaseDatabase):
    encoding = "utf-8"
    default_expire: Optional[Union[int, timedelta]] = 86400
    server: "redis.Redis"

    def __init__(
        self,
        server: "redis.Redis",
        encoding="utf-8",
        default_expire: Optional[Union[int, timedelta]] = 86400,
    ):
        self.default_expire = default_expire
        self.encoding = encoding
        self.server = server

    def get(self, key: str) -> Optional[str]:
        content = self.server.get(key)
        return content.decode(self.encoding) if content else None

    def set(self, key: str, value: str, expire: int = None):
        if not self.server.set(key, value):
            raise SetError

        if expire and not self.server.expire(key, expire):
            raise ExpireError
        elif self.default_expire and not self.server.expire(
            key, self.default_expire
        ):
            raise ExpireError

    def delete(self, key: str):
        try:
            self.server.delete(key)
        except redis.RedisError:
            raise DeleteError
