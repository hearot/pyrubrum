# Pyrubrum - An intuitive framework for creating Telegram bots
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyrubrum.
#
# Pyrubrum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrubrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyrubrum. If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
from typing import Optional

from pyrubrum.types import Types


class BaseDatabase(ABC):
    """Basic representation of a database, which, by definition, implements the
    three fundamental operations `delete`, `get` and `set`.

    The purpose of this class is to give a general interface for a database,
    as it does not implement anything.

    A sample implementation of this interface is `~pyrubrum.RedisDatabase`.

    Note:
        In order to create a subclass or to access this interface, you will
        need to implement all the abstract methods, which are `delete`, `get`
        and `set`. Otherwise, you will get an error.
    """

    @abstractmethod
    def get(self, key: str) -> str:
        """This abstract method is intended to be implemented in order to get the value
        which is stored with a certain key inside the database.

        Parameters:
            key (str): The key you are retrieving the value of.

        Returns:
            Optional[str]: The value which is associated to the key.

        Raises:
            GetError: If an error occured while retrieving the key from the
                database.
            NotFoundError: If the provided key is not found.
        """
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: str, expire: Optional[Types.Expire] = None):
        """This abstract method is intended to be implemented in order to assign a
        value to a certain key inside the database. It may even be marked with
        an expire as to avoid having too much unused data stored inside the
        database.

        Parameters:
            key (str): The key you are adding or updating the value of.
            value (str): The value which is being assigned to the key.
            expire (Optional[Types.Expire]): The expire in seconds or as a
                `timedelta` object. A key is set not to expire if ``False`` is
                provided for this argument. Defaults to ``None``.

        Raises:
            ExpireError: If an error occured while setting the expire for the
                key.
            SetError: If an error occured while inserting the key into the
                database.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str):
        """This abstract method is intended to be implemented in order to delete a
        certain key from the database, together with its stored value.

        Parameters:
            key (str): The key which is being deleted from the database,
                together with its linked data.

        Raises:
            DeleteError: If an error occured while deleting the key.
            NotFoundError: If the provided key is not found.
        """
        raise NotImplementedError
