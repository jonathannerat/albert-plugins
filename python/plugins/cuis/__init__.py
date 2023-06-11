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
OPEN_IMAGE_SCRIPT = CUIS_DIR + "/open-image"
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
        search: str = query.string.strip().lower()
        results = [self.itemForImage(i) for i in self.cuisImagesMatching(search)]

        if len(results):
            query.add(results)
        else:
            query.add(self.createImageItem(query.string.strip()))

    def cuisImagesMatching(self, search: str) -> list[str]:
        image_pattern = "*" + IMAGE_EXT
        images: list[str] = []

        for root, _, filenames in os.walk(CUIS_IMAGES_DIR):
            for filename in fnmatch.filter(filenames, image_pattern):
                filename_noext = self.filenameWithoutExtension(filename)
                if search in filename_noext.lower():
                    images.append(os.path.join(root, filename))

        images.sort()

        return images

    def itemForImage(self, image_path: str):
        relative_filename_noext = self.filenameWithoutExtension(
            image_path[len(CUIS_IMAGES_DIR) + 1 :]
        )

        return Item(
            id=relative_filename_noext,
            icon=ICON,
            text=relative_filename_noext,
            subtext=image_path,
            completion="cuis " + relative_filename_noext,
            actions=[
                Action(
                    "open",
                    "Open",
                    lambda: runDetachedProcess([OPEN_IMAGE_SCRIPT, image_path]),
                )
            ],
        )

    def createImageItem(self, name: str):
        image_path = os.path.join(CUIS_IMAGES_DIR, name + IMAGE_EXT)

        return Item(
            id="new-image",
            icon=ICON,
            text=name,
            subtext=image_path,
            completion="cuis " + name,
            actions=[
                Action(
                    "create",
                    "Create CUIS Image",
                    lambda: runDetachedProcess([OPEN_IMAGE_SCRIPT, image_path]),
                )
            ],
        )

    def filenameWithoutExtension(self, path: str):
        return path[: -len(IMAGE_EXT)]
