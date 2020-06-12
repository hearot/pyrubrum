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

from typing import Optional

from .base_database import BaseDatabase
from .base_database import Expire
from .errors import DeleteError


class DictDatabase(dict, BaseDatabase):
    """Reduced implementation of a database using a dictionary, without the
    assignment of an expire to a key whenever one is added to the database.

    Warning:
        It not recommended to use this in production, as it does not implement
        expires, while other implementations, such as `RedisDatabase`, does.
        In addition, any stored data will be erased as soon as the program
        stops executing.
        This implementation might be useful only in development and testing
        mode.
    """

    def get(self, key: str) -> Optional[str]:
        """Get the value which is stored with a certain key inside the database,
        if any. Otherwise, it will just return ``None``.

        This method will query the key using `dict.get`, which automatically
        returns ``None`` if the key has not been found.

        Args:
            key (str): The key you are retrieving the value of from the
                dictionary.

        Returns:
            Optional[str]: The value which is associated to the key in the
                dictionary, if any. Otherwise, it is set to be ``None``.
        """
        return dict.get(self, key)

    def set(self, key: str, value: str, expire: Optional[Expire] = None):
        """Assign a value to a certain key inside the database. Note that this
        implementation ignores the setting of any expires.

        This method will assign the provided value to the key using
        `dict.update`.

        Args:
            key (str): The key you are adding or updating the value of.
            value (str): The value which is being assigned to the key.
            expire (Optional[Expire]): It gets ignored by this implementation.
                Defaults to ``None``.
        """

        self.update({key: value})

    def delete(self, key: str):
        """Delete a certain key from the database, together with its stored value.

        This method will delete the provided key from the database using
        `dict.pop`.

        Args:
            key (str): The key which is being deleted from the database,
                together with its linked data.

        Raises:
            DeleteError: If no key was found.
        """
        try:
            self.pop(key)
        except KeyError:
            raise DeleteError
