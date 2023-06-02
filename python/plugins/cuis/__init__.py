# -*- coding: utf-8 -*-

import fnmatch
import os
from albert import *

md_iid = "0.5"
md_version = "0.1"
md_name = "Cuis"
md_description = "Launch Cuis images"
md_bin_dependencies = []
md_maintainers = "@jonathannerat"
md_license = "MIT"

HOME_DIR = os.environ["HOME"]
CUIS_DIR = HOME_DIR + "/files/cuis-university"
CUIS_IMAGES_DIR = CUIS_DIR + "/images"
ICON = ["/home/jt/files/cuis-university/favicon.ico"]
IMAGE_EXT = ".image"


class Plugin(QueryHandler):
    def id(self):
        return md_id

    def name(self):
        return md_name

    def description(self):
        return md_description

    def synopsis(self):
        return "<cuis-image>"

    def defaultTrigger(self):
        return "cuis "

    def handleQuery(self, query):
        results = []
        search: str = query.string.strip().lower()

        for image in self.getCuisImagesFromQuery(search):
            name = image[image.rindex("/")+1:image.rindex(IMAGE_EXT)]

            results.append(
                Item(
                    id=name,
                    icon=ICON,
                    text=name,
                    subtext=image,
                    completion="cuis " + name,
                    actions=[
                        Action(
                            "open",
                            "Open",
                            lambda: runDetachedProcess(
                                [f"{CUIS_DIR}/xdg-open.sh", image[len(CUIS_DIR)+1:]]
                            ),
                        )
                    ],
                )
            )

        query.add(results)

    def getCuisImagesFromQuery(self, search: str) -> list[str]:
        pat = "*" + IMAGE_EXT
        images: list[str] = []

        for root, _, filenames in os.walk(CUIS_IMAGES_DIR):
            for filename in fnmatch.filter(filenames, pat):
                if search in filename[: -len(IMAGE_EXT)].lower():
                    images.append(os.path.join(root, filename))

        return sorted(images, key=lambda s: s.lower())
