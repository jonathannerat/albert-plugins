# -*- coding: utf-8 -*-

import fnmatch
import os
from albert import Item, QueryHandler, Action, runDetachedProcess

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
ICON = "/home/jt/files/cuis-university/favicon.ico"
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
            results.append(self.itemForImage(image))

        query.add(results)

    def getCuisImagesFromQuery(self, search: str) -> list[str]:
        pat = "*" + IMAGE_EXT
        images: list[str] = []

        for root, _, paths in os.walk(CUIS_IMAGES_DIR):
            for image in fnmatch.filter(paths, pat):
                filename  = self.filenameWithoutExtension(image)
                if search in filename.lower():
                    images.append(os.path.join(root, filename))

        return sorted(images, key=lambda s: s.lower())

    def itemForImage(self, image):
        name = self.filenameWithoutExtension(image)

        return Item(
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
                        [f"{CUIS_DIR}/xdg-open.sh", image[len(CUIS_DIR) + 1 :]]
                    ),
                )
            ],
        )

    def filenameWithoutExtension(self, image: str):
        return image[len(CUIS_IMAGES_DIR) + 1 : -len(IMAGE_EXT)]
