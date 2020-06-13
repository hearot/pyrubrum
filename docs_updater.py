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

import inspect
import os
import re
from collections import defaultdict

import pyrubrum

CLASS_ATTRIBUTES = ":members:"
FILE_EXTENSION = ".rst"
INDEX_TEMPLATE = """
{title}
{separators}

.. toctree::
    :caption: Defined objects

{tree}
"""
SPECIAL_ENTITIES = ["Button", "Element", "Keyboard", "Node"]
TEMPLATE = """{title}
{separators}

.. auto{object_type}:: pyrubrum.{name}
{attributes}
"""

entities = defaultdict(list)


def get_file_name(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


for entity in filter(lambda e: not e.startswith("_"), dir(pyrubrum)):
    variable = getattr(pyrubrum, entity)

    if hasattr(variable, "__package__"):
        continue

    attributes = " " * 4

    if inspect.isclass(variable):
        object_type = "class"
        attributes += CLASS_ATTRIBUTES
    elif inspect.isfunction(variable):
        object_type = "function"
    elif isinstance(variable, Exception):
        object_type = "exception"

    content = TEMPLATE.format(
        attributes=attributes.rstrip(),
        name=entity,
        object_type=object_type,
        title=entity,
        separators="=" * len(entity),
    ).strip()
    filename = get_file_name(entity) + FILE_EXTENSION
    dirname = os.path.dirname(os.path.realpath(__file__))

    if "Error" in entity:
        directory = "database/errors"
    elif "Database" in entity:
        directory = "database"
    elif "Handler" in entity:
        directory = "handlers"
    elif "Menu" in entity:
        directory = "menus"
    elif entity[0].lower() == entity[0] or entity in SPECIAL_ENTITIES:
        directory = "utils"
    else:
        continue

    entities[directory].append(entity)

    path = os.path.join(dirname, "docs", "source", "api", directory, filename)

    with open(path, mode="w") as text:
        text.write(content)

for directory, elements in entities.items():
    tree = ""
    title = directory.replace("/", " ").title()

    for element in elements:
        tree += " " * 4 + get_file_name(element) + "\n"

    index = INDEX_TEMPLATE.format(
        title=title, separators="=" * len(title), tree=tree
    )

    path = os.path.join(
        dirname, "docs", "source", "api", directory, "index.rst"
    )

    with open(path, mode="w") as text:
        text.write(index.strip())
