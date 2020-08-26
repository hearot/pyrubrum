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

from typing import Any, Dict

from pyrogram import Client

from pyrubrum.database.base_database import BaseDatabase
from pyrubrum.database.errors.not_found_error import NotFoundError

try:
    import orjson as json  # noqa
except (ImportError, ModuleNotFoundError):
    import json


class User(dict):
    """Representation of a user, which behaves like a dictionary and
    has got, by definition, a key named `user_id` which is the unique
    identifier of the user.
    """

    def delete(self, database: BaseDatabase):
        """Given a database, delete this object from it.

        Parameters:
            database (BaseDatabase): The database from which the user is being
                deleted.
        """
        database.delete("user_" + str(self["user_id"]))

    @classmethod
    def get(cls, database: BaseDatabase, user_id: int) -> "User":
        """Get a user from a given database seeking a key that follows
        this pattern::

            user_[USER_ID]

        Parameters:
            database (BaseDatabase): The database which is queried to seek
                the user.
            user_id (int): The unique identifier of the user that is being
                seeked.

        Returns:
            User: The retrieved user.
        """
        return cls.parse(database.get("user_" + str(user_id)))

    @classmethod
    def get_or_create(cls, database: BaseDatabase, user_id: int) -> "User":
        """Get a user from a given database, if any. Otherwise, a new user
        is created using the following pattern as key::

            user_[USER_ID]

        Parameters:
            database (BaseDatabase): The database which is queried to seek
                the user.
            user_id (int): The unique identifier of the user that is being
                seeked.

        Returns:
            User: The retrieved user.
        """
        try:
            return cls.parse(database.get("user_" + str(user_id)))
        except NotFoundError:
            user = cls({"user_id": user_id})
            user.save(database)
            return user

    @classmethod
    def parse(cls, data: str) -> "User":
        """Automatically create a new `User` object from a JSON object.

        Parameters:
            data (str): The JSON object as string.

        Returns:
            User: The generated `User` object.
        """

        return cls(json.loads(data))

    @classmethod
    def preliminary(
        cls,
        handler: "ParameterizedBaseHandler",  # noqa
        client: Client,
        context: Any,
        parameters: Dict[str, Any] = None,
    ):
        """Automatically retrieve the `User` object relying on the identifier of the
        user who made the query and assign it to ``context.current_user``.

        Parameters:
            handler (BaseHandler): The handler which coordinates the management
                of the menus.
            client (Client): The client which is linked to the handler.
            context (CallbackQuery): The callback query for which the button is
                generated.
            parameters (Optional[Dict[str, Any]]): The parameters which were
                passed to the handler. Defaults to ``None``.
        """
        context.current_user = cls.get_or_create(
            handler.database, context.from_user.id
        )

    def save(self, database: BaseDatabase):
        """Save the `User` object to the the database using the following pattern
        as key::

            user_[USER_ID]

        Parameters:
            database (BaseDatabase): The database to which this object is
                being saved.
        """
        database.set("user_" + str(self["user_id"]), json.dumps(self))
