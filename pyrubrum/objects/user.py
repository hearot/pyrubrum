# Pyrubrum - An intuitive framework for creating Telegram bots
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyrubrum.
#
# Pyrubrum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrubrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyrubrum. If not, see <http://www.gnu.org/licenses/>.

from typing import Any
from typing import Dict

from pyrogram import Client

from pyrubrum.database.base_database import BaseDatabase
from pyrubrum.database.errors.not_found_error import NotFoundError

try:
    import orjson as json  # noqa
except (ImportError, ModuleNotFoundError):
    import json


class User(dict):
    def delete(self, database: BaseDatabase):
        database.delete(self["user_id"])

    @classmethod
    def get(cls, database: BaseDatabase, user_id: int) -> "User":
        return cls.parse(database.get("user_" + str(user_id)))

    @classmethod
    def get_or_create(cls, database: BaseDatabase, user_id: int) -> "User":
        try:
            return cls.parse(database.get("user_" + str(user_id)))
        except NotFoundError:
            user = cls({"user_id": user_id})
            user.save(database)
            return user

    @classmethod
    def parse(cls, data: str) -> "User":
        return cls(json.loads(data))

    @classmethod
    def preliminary(
        cls,
        handler: "ParameterizedBaseHandler",  # noqa
        client: Client,
        context: Any,
        parameters: Dict[str, Any] = None,
    ):
        context.current_user = cls.get_or_create(
            handler.database, context.from_user.id
        )

    def save(self, database: BaseDatabase):
        database.set("user_" + str(self["user_id"]), json.dumps(self))
