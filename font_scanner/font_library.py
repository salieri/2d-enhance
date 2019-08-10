import itertools as it, glob
import os
import json
from typing import Iterable
import random

from PIL import ImageFont

class FontLibrary:
    def __init__(self, config: dict, base_path: str):
        self.config = config
        self.base_path = base_path
        self.file_extensions = ['*.oft', '*.ttf']
        self.library = {}


    def scan_filenames(self) -> Iterable:
        return it.chain.from_iterable(glob.iglob(os.path.join(self.base_path, ext), recursive=True) for ext in self.file_extensions)


    def scan(self, base_path: str) -> dict:
        fonts = []

        for filename in self.scan_filenames():
            ff = {
                "variations": []
            }

            for size in [9, 10, 12, 14, 18, 24, 32, 48]:
                ff['variations'].append(ImageFont.truetype(filename, size=size))

            (family, style) = ff['variations'][0].getname()
            ff['name'] = f"{family}-{style}"

            fonts.append(ff)

        self.library = {
            'type': 'nn-2d-font-scan',
            'base_path': base_path,
            'fonts': fonts
        }

        return self.library


    def get_font(self, family, index):
        return self.library['fonts'][family]['variations'][index]


    def get_random_font(self) -> ImageFont:
        family = random.choice(self.library['fonts'])

        return random.choice(family['variations'])


    def load(self, filename: str) -> dict:
        with open(filename, 'r') as fp:
            self.library = json.load(fp)

            return self.library


    def save(self, filename: str, scan_results: dict) -> None:
        with open(filename, 'w') as fp:
            json.dump(scan_results, fp)

