import itertools as it, glob
import os
import json

from .image_analyzer import ImageAnalyzer

class ImageLibrary:
    def __init__(self, config, base_path):
        self.config = config
        self.base_path = base_path
        self.file_extensions = ['*.jpg', '*.png', '*.gif']


    def scan_filenames(self):
        return it.chain.from_iterable(glob.iglob(os.path.join(self.base_path, ext), recursive=True) for ext in self.file_extensions)


    def scan(self, base_path):
        backgrounds = []
        sprites = []
        native = self.config['processor']['native']
        native_width = native['width']
        native_height = native['height']

        for filename in self.scan_filenames():
            ia = ImageAnalyzer(filename)

            details = ia.analyze()

            if (details['solid'] is True) and (details['width'] >= native_width) and (details['height'] >= native_height):
                backgrounds.append(details)
            else:
                sprites.append(details)

        return {
            'type': 'nn-2d-enhance-scan',
            'base_path': base_path,
            'backgrounds': backgrounds,
            'sprites': sprites
        }


    def load(self, filename):
        with open(filename, 'r') as fp:
            return json.load(fp)


    def save(self, filename, scan_results):
        with open(filename, 'w') as fp:
            json.dump(scan_results, fp)

