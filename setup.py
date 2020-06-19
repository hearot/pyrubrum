#!/usr/bin/env python3
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

import re

from setuptools import find_packages
from setuptools import setup

GITHUB_REPOSITORY = "https://github.com/hearot/pyrubrum/blob/v%s/"


with open("fast-requirements.txt", encoding="utf-8") as r:
    fast_requirements = [p.strip() for p in r]

with open("pyrubrum/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", encoding="utf-8") as f:
    long_description = f.read().replace("./", GITHUB_REPOSITORY % version)

with open("requirements.txt", encoding="utf-8") as r:
    requirements = [p.strip() for p in r]

setup(
    author="Hearot",
    author_email="gabriel@hearot.it",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    description="An intuitive framework for creating Telegram bots",
    extras_require={"fast": fast_requirements},
    install_requires=requirements,
    keywords="bot bots chat messenger mtproto pyrogram python telegram",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="Pyrubrum",
    packages=find_packages(),
    project_urls={
        "Tracker": "https://github.com/hearot/pyrubrum/issues",
        "Source": "https://github.com/hearot/pyrubrum",
    },
    python_requires=">=3.6.*",
    url="https://github.com/hearot/pyrubrum",
    version=version,
)
