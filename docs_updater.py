#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import inspect
import os
import re
import shutil
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
KEYBOARD_ENTITIES = ["Button", "Element", "Keyboard"]
OBJECT_ENTITIES = ["User"]
TEMPLATE = """{title}
{separators}

.. auto{object_type}:: pyrubrum.{name}
{attributes}
"""
TREE_ENTITIES = ["Node", "recursive_add", "transform"]

entities = defaultdict(list)

try:
    shutil.rmtree("docs/source/api")
except (OSError, PermissionError):
    pass


def get_file_name(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


for entity in filter(lambda e: not e.startswith("_"), dir(pyrubrum)):
    variable = getattr(pyrubrum, entity)

    if hasattr(variable, "__package__"):
        continue

    attributes = " " * 4

    if inspect.isclass(variable):
        if issubclass(variable, Exception):
            object_type = "exception"
        else:
            object_type = "class"

        attributes += CLASS_ATTRIBUTES
    elif inspect.isfunction(variable):
        object_type = "function"
    else:
        object_type = "data"

    content = TEMPLATE.format(
        attributes=attributes.rstrip(),
        name=entity,
        object_type=object_type,
        title=entity,
        separators="=" * len(entity),
    ).strip()
    filename = get_file_name(entity) + FILE_EXTENSION
    dirname = os.path.dirname(os.path.realpath(__file__))
    name = entity.lower()

    if "error" in name:
        directory = "database/errors"
    elif "style" in name:
        directory = "styles"
    elif "database" in name:
        directory = "database"
    elif "handler" in name:
        directory = "handlers"
    elif "menu" in name:
        directory = "menus"
    elif entity in KEYBOARD_ENTITIES:
        directory = "keyboard"
    elif entity in TREE_ENTITIES:
        directory = "tree"
    elif entity in OBJECT_ENTITIES:
        directory = "objects"
    else:
        directory = "types"

    entities[directory].append(entity)

    path = os.path.join(dirname, "docs", "source", "api", directory)

    try:
        os.makedirs(path, exist_ok=True)
    except (FileNotFoundError, OSError, PermissionError):
        pass

    path = os.path.join(path, filename)

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

    path = os.path.join(dirname, "docs", "source", "api", directory)

    try:
        os.makedirs(path, exist_ok=True)
    except (FileNotFoundError, OSError, PermissionError):
        pass

    path = os.path.join(path, "index.rst")

    with open(path, mode="w") as text:
        text.write(index.strip())
