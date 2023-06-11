# -*- coding: utf-8 -*-

import os
import csv
import dataclasses
import re
from albert import (
    QueryHandler,
    Action,
    Item,
    openUrl,
    setClipboardText,
    sendTrayNotification,
)

md_iid = "0.5"
md_version = "0.1"
md_name = "Bookmarks"
md_description = "Open bookmarks from CSV"
md_bin_dependencies = []
md_maintainers = "@jonathannerat"
md_license = "MIT"

BOOKMARKS_CSV = os.environ["HOME"] + "/notebook/bookmarks.csv"
ICON = ["/usr/share/icons/Papirus-Dark/16x16/actions/bookmarks.svg"]


@dataclasses.dataclass()
class Bookmark:
    id: str
    name: str
    url: str
    tags: str
    desc: str

    def matches(self, search: str):
        if search in self.name.lower():
            return True

        if search in self.url.lower():
            return True

        if search in self.tags.lower():
            return True

        return False


class Plugin(QueryHandler):
    def id(self):
        return md_id

    def name(self):
        return md_name

    def description(self):
        return md_description

    def synopsis(self):
        return "<bookmark>"

    def defaultTrigger(self):
        return "bm "

    def handleQuery(self, query):
        search: str = query.string.strip()
        results = [self.itemForBookmark(b) for b in self.bookmarksMatching(search)]

        if len(results) > 0:
            query.add(results)
        elif re.match("^https?://", search) is not None:
            query.add(
                Item(
                    icon=ICON,
                    text="Create bookmark",
                    subtext=search,
                    completion=f"bm {search}",
                    actions=[
                        Action("create", "Create Bookmark", lambda: openUrl(search)),
                    ],
                )
            )

    def bookmarksMatching(self, search: str) -> list[Bookmark]:
        results = []

        with open(BOOKMARKS_CSV, "r") as bmfile:
            bmreader = csv.reader(bmfile)
            skip_header = True

            for row in bmreader:
                if skip_header:
                    skip_header = False
                    continue

                bm = Bookmark(*row)

                if bm.matches(search.lower()):
                    results.append(bm)

        return results

    def itemForBookmark(self, bm: Bookmark):
        return Item(
            id=bm.id,
            icon=ICON,
            text=bm.name,
            subtext=bm.url,
            completion=f"bm {bm.url}",
            actions=[
                Action("open", "Open URL", lambda: openUrl(bm.url)),
                Action("copy", "Copy URL", lambda: setClipboardText(bm.url)),
            ],
        )
