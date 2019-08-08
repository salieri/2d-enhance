import random
import os

import PIL
from PIL import Image, ImageMode


class ImageProcessor:
    def __init__(self, config, run_opts, id):
        self.config = config
        self.run_opts = run_opts
        self.id = id

        self.grid = {
            'width': random.randint(self.config['content']['grid'].content.grid.size.min.width, self.config.content.grid.size.max.width),
            'height': random.randint(self.config.content.grid.size.min.height, self.config.content.grid.size.max.height)
        }

        self.size = {
            'width': self.config.processor.native.size.width,
            'height': self.config.processor.native.size.height
        }


    def generate(self):
        self.im = Image.new('RGBA', (self.size['width'], self.size['height']), color=(0, 0, 0, 0))


    def save(self):
        self.get_output_path()


    def save_variation(self, variation, output_path):
        resized = self.im.resize((variation.width, variation.height), resample=Image.LANCZOS)
        effects = self.process_variation_effects(variation, resized)

        out = effects.convert(variation.mode)

        out.save(os.path.join(output_path, self.get_variation_filename(variation)), effects)


    def process_variation_effects(self, variation, im):
        for v in variation.effects:


        return im


    def get_variation_filename(self, variation):
        return f"{self.id}.{variation.name}.{variation.format}"


    def get_output_path(self):
        ext_path = str(self.id)[-self.run_opts.output_depth].zfill(self.run_opts.output_depth).join(os.path.sep)

        return os.path.join(self.run_opts.output, ext_path)
