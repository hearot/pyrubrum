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

from collections import defaultdict
from git import Repo
import re
import os

CHANGELOG_FILE = "CHANGELOG.md"
CONVENTIONAL_COMMITS_REGEX = r"^([a-z]+)(!)?(?:\([a-z]+\)+)?: ([^\n]+)+$"

match_commit = re.compile(CONVENTIONAL_COMMITS_REGEX)
version_tree = defaultdict(lambda: defaultdict(list))


def main():
    repo = Repo(os.path.dirname(os.path.realpath(__file__)))

    tags_list = sorted(repo.tags,
                       key=lambda t: t.commit.committed_date) + ['']
    tags = iter(tags_list)
    tag = ""
    next_tag = str(next(repo.iter_commits(max_count=1,
                                          max_parents=0)))

    try:
        while True:
            tag = next_tag
            next_tag = str(next(tags))

            print(">>> FROM %s TO %s <<<" % (tag, next_tag))

            commits = repo.iter_commits(
                str(tag) + "..." + str(next_tag),
                reverse=True)

            for commit in commits:
                match = match_commit.search(commit.message.split('\n')[0])

                if match:
                    type_commit = match.group(1)
                    breaking_change = match.group(2)
                    breaking_change = (breaking_change if breaking_change
                                       else "")
                    brief_message = match.group(3)

                    if breaking_change == "!":
                        version_tree[next_tag]['Breaking changes'].append(
                            "%s (%s)" % (brief_message.capitalize(),
                                         str(commit))
                        )
                    else:
                        version_tree[next_tag][
                            type_commit.capitalize()].append(
                            "%s (%s)" % (brief_message.capitalize(),
                                         str(commit))
                        )

                    print("    " + type_commit + breaking_change + ":",
                          brief_message)
    except StopIteration:
        pass

    if '' in version_tree:
        version_tree['Unreleased'] = version_tree.pop('')

    changelog_file = (os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   CHANGELOG_FILE))

    with open(changelog_file, 'w', encoding="utf-8") as f:
        f.write("# Changelog\n\n")

        for version in map(str, reversed(tags_list)):
            version = version if version else 'Unreleased'
            types = version_tree[version]

            f.write("\n## %s\n" % version)

            for type_commit, commits in types.items():
                # print(type_commit, commits)
                f.write("\n### %s\n\n" % type_commit)

                for commit in commits:
                    f.write("   - %s\n" % commit)


if __name__ == '__main__':
    main()
