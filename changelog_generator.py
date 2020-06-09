#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import os
import re
import sys
from collections import defaultdict

from git import Repo

CHANGELOG_FILE = "CHANGELOG.md"
CONVENTIONAL_COMMITS_REGEX = r"^([a-z]+)(!)?(?:\([a-z]+\)+)?: ([^\n]+)+$"
TITLES = {
    "build": "Build changes",
    "chore": "Other changes",
    "docs": "Documentation",
    "feat": "New features",
    "fix": "Fixes",
}

match_commit = re.compile(CONVENTIONAL_COMMITS_REGEX)

titles = defaultdict(lambda: "New features")
titles.update(TITLES)

version_tree = defaultdict(lambda: defaultdict(list))


def generate_changelog(last_commit_message: str):
    repo = Repo(os.path.dirname(os.path.realpath(__file__)))

    tags_list = sorted(repo.tags, key=lambda t: t.commit.committed_date) + [""]
    tags = iter(tags_list)
    tag = ""
    next_tag = str(next(repo.iter_commits(max_count=1, max_parents=0)))

    try:
        while True:
            tag = next_tag
            next_tag = str(next(tags))

            print(">>> FROM %s TO %s <<<" % (tag, next_tag))

            commits = repo.iter_commits(
                str(tag) + "..." + str(next_tag), reverse=True
            )

            for commit in commits:
                match = match_commit.search(commit.message.split("\n")[0])

                if match:
                    type_commit = match.group(1)
                    breaking_change = match.group(2)
                    breaking_change = (
                        breaking_change if breaking_change else ""
                    )
                    brief_message = match.group(3)

                    if breaking_change == "!":
                        version_tree[next_tag]["Breaking changes"].append(
                            "%s (%s)"
                            % (brief_message.capitalize(), str(commit))
                        )
                    else:
                        version_tree[next_tag][titles[type_commit]].append(
                            "%s (%s)"
                            % (brief_message.capitalize(), str(commit))
                        )

                    print(
                        "    " + type_commit + breaking_change + ":",
                        brief_message,
                    )
    except StopIteration:
        pass

    if "" in version_tree:
        version_tree["Current version"] = version_tree.pop("")

    match = match_commit.search(last_commit_message)

    if match:
        type_commit = match.group(1)
        breaking_change = match.group(2)
        breaking_change = breaking_change if breaking_change else ""
        brief_message = match.group(3)

        if breaking_change == "!":
            version_tree["Current version"]["Breaking changes"].append(
                "%s (%s)" % (brief_message.capitalize(), str(commit))
            )
        else:
            version_tree["Current version"][titles[type_commit]].append(
                "%s (%s)" % (brief_message.capitalize(), str(commit))
            )

        print(
            "LAST COMMIT MESSAGE: " + type_commit + breaking_change + ":",
            brief_message,
        )

    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), CHANGELOG_FILE
    )

    with open(changelog_file, "w", encoding="utf-8") as f:
        f.write("# Changelog\n\n## Table of contents\n\n")

        for version in map(str, reversed(tags_list)):
            version = version if version else "Current version"
            f.write(
                "   * [%s](#%s)\n"
                % (version, version.replace(".", "").replace(" ", "-"))
            )

        for version in map(str, reversed(tags_list)):
            version = version if version else "Current version"
            types = version_tree[version]

            f.write("\n## %s\n" % version)

            for type_commit in sorted(types.keys()):
                commits = types[type_commit]

                f.write("\n### %s\n\n" % type_commit)

                for commit in sorted(commits):
                    f.write("   - %s\n" % commit)

    repo.git.add(CHANGELOG_FILE)
    repo.git.update_index(CHANGELOG_FILE, add=True)


if __name__ == "__main__":
    with open(sys.argv[-1], "r") as commit_message_file:
        commit_message = commit_message_file.read().split("\n")[0]

    generate_changelog(commit_message)
    sys.exit(0)
