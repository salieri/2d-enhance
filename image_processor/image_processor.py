import random
import os
from math import floor
from PIL import Image

from .effect_processor import EffectProcessor
from .content_processor import ContentProcessor

import util


class ImageProcessor:
    def __init__(self, config, run_opts, im_library, font_library, id):
        self.config = config
        self.run_opts = run_opts
        self.im_library = im_library
        self.font_library = font_library
        self.id = id

        grid_size = self.config['content']['grid']['size']
        native_size = self.config['processor']['native']['size']

        self.grid = {
            'width': random.randint(grid_size['min']['width'], grid_size['max']['width']),
            'height': random.randint(grid_size['min']['height'], grid_size['max']['height'])
        }

        self.size = {
            'width': native_size['width'],
            'height': native_size['height']
        }


    def generate(self):
        self.im = Image.new('RGBA', (self.size['width'], self.size['height']), color=(0, 0, 0, 0))

        self.generate_background()
        self.generate_content()


    def generate_background(self):
        bg_config = self.config['background']

        if util.should(bg_config) is False:
            return

        bg = random.choice(self.im_library['backgrounds'])
        bgim = Image.open(bg['filename']).convert('RGBA')

        ep = EffectProcessor()

        bgfxim = ep.process_effects(bgim, bg_config['effects'])

        pos_x = -random.randint(0, max(0, bgim.width - self.im.width))
        pos_y = -random.randint(0, max(0, bgim.height - self.im.height))

        self.im.paste(bgfxim, box=(pos_x, pos_y))


    def generate_content(self):
        for col_index in range(self.grid['width'] * self.grid['height']):
            bounding_box = self.get_bounding_box(col_index)

            cp = ContentProcessor(self.im, self.im_library, self.font_library, bounding_box)

            cp.process_content(self.config['content']['types'])


    def get_bounding_box(self, col_index):
        grid_width = self.grid['width']
        grid_height = self.grid['height']

        col_x = col_index % grid_width
        col_y = floor(col_index / grid_width)

        pixel_width = self.size['width'] / grid_width
        pixel_height = self.size['height'] / grid_height

        x = col_x * pixel_width
        y = col_y * pixel_height

        return {
            'x': round(x),
            'y': round(y),
            'x2': round(x + pixel_width - 1),
            'y2': round(y + pixel_height - 1),
            'cx': round(x + pixel_width / 2),
            'cy': round(y + pixel_height / 2),
            'width': pixel_width,
            'height': pixel_height
        }


    def save(self):
        for variation in self.config['output']:
            self.save_variation(variation)


    def save_variation(self, variation):
        resized = self.im.resize((variation['size']['width'], variation['size']['height']), resample=Image.LANCZOS)
        effects = self.process_variation_effects(variation, resized)

        out = effects.convert(variation.mode)
        output_path = self.get_output_path()

        os.makedirs(output_path, exist_ok=True)
        out.save(os.path.join(output_path, self.get_variation_filename(variation)), effects)


    def process_variation_effects(self, variation, im):
        ep = EffectProcessor()

        return ep.process_effects(im, variation['effects'])


    def get_variation_filename(self, variation):
        return f"{self.id}.{variation['name']}.{variation['format']}"


    def get_output_path(self):
        output_depth=self.run_opts['output_depth']

        ext_path = str(self.id)[-output_depth].zfill(output_depth).join(os.path.sep)

        return os.path.join(self.run_opts['output'], ext_path)
