import itertools as it, glob
import os
import json
from PIL import ImageFont

class FontLibrary:
    def __init__(self, config, base_path):
        self.config = config
        self.base_path = base_path
        self.file_extensions = ['*.oft', '*.ttf']


    def scan_filenames(self):
        return it.chain.from_iterable(glob.iglob(os.path.join(self.base_path, ext), recursive=True) for ext in self.file_extensions)


    def scan(self, base_path):
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

        return {
            'type': 'nn-2d-font-scan',
            'base_path': base_path,
            'fonts': fonts
        }


    def load(self, filename):
        with open(filename, 'r') as fp:
            return json.load(fp)


    def save(self, filename, scan_results):
        with open(filename, 'w') as fp:
            json.dump(scan_results, fp)

