# -*- coding: utf-8 -*-

import os
import csv
import dataclasses
from typing import Callable
from albert import *

md_iid = "0.5"
md_version = "0.1"
md_name = "Bookmarks"
md_description = "Open bookmarks from CSV"
md_bin_dependencies = []
md_maintainers = "@jonathannerat"
md_license = "MIT"

BOOKMARKS_CSV = os.environ["HOME"] + "/notebook/bookmarks.csv"
ICON = ["/usr/share/icons/Papirus-Dark/16x16/actions/bookmarks.svg"]


@dataclasses.dataclass(init=False)
class Bookmark:
    id: str
    name: str
    url: str
    tags: list[str]
    desc: str

    def __init__(self, row: list[str]) -> None:
        self.id = row[0]
        self.name = row[1]
        self.url = row[2]
        self.desc = row[4]
        self.tags = row[3].split(",")


QueryFilter = Callable[[Bookmark], bool]


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
        search = query.string.strip().lower()
        query_filter: QueryFilter = (
            lambda bm: search in (bm.name + bm.url + bm.desc).lower()
        )
        results: list[Item] = []

        for bm in self.getBookmarks(query_filter if search else None):
            results.append(
                Item(
                    id=bm.id,
                    icon=ICON,
                    text=bm.name,
                    subtext=bm.url,
                    completion=f"bookmark {bm.url}",
                    actions=[
                        Action("open", "Open URL", lambda: openUrl(bm.url)),
                        Action("copy", "Copy URL", lambda: setClipboardText(bm.url)),
                    ],
                )
            )

        query.add(results)

    def getBookmarks(self, query_filter: QueryFilter | None) -> list[Bookmark]:
        results = []

        with open(BOOKMARKS_CSV, "r") as bmfile:
            bmreader = csv.reader(bmfile)
            skip_header = True

            for row in bmreader:
                if skip_header:
                    skip_header = False
                    continue

                bm = Bookmark(row)

                if query_filter is None or query_filter(bm):
                    results.append(bm)

        return results
