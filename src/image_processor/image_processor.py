import random
import os
from math import floor
from PIL import Image

from .bounding_box import BoundingBox
from .effect_processor import EffectProcessor
from .content_processor import ContentProcessor
from .background_processor import BackgroundProcessor

from src.config import Config, ConfigOutputTarget, RunOpts
from src.image_scanner import ImageLibrary
from src.font_scanner import FontLibrary

class ImageProcessor:
    config: Config
    run_opts: RunOpts
    im_library: ImageLibrary
    font_library: FontLibrary
    id: str

    def __init__(self, config: Config, run_opts: RunOpts, im_library: ImageLibrary, font_library: FontLibrary, id: str):
        self.config = config
        self.run_opts = run_opts
        self.im_library = im_library
        self.font_library = font_library
        self.id = id

        grid_size = config.content.grid.size

        self.grid = {
            'width': random.randint(grid_size.min.width, grid_size.max.width),
            'height': random.randint(grid_size.min.height, grid_size.max.height)
        }


    def generate(self) -> None:
        self.im = self.generate_background()

        self.generate_content()


    def generate_background(self) -> Image.Image:
        native_size = self.config.processor.native.size

        bp = BackgroundProcessor(self.im_library, native_size.width, native_size.height)

        return bp.process_background(self.config.background.types)


    def generate_content(self) -> None:
        for col_index in range(self.grid['width'] * self.grid['height']):
            bounding_box = self.get_bounding_box(col_index)

            cp = ContentProcessor(self.im, self.im_library, self.font_library, bounding_box)

            cp.process_content(self.config.content.types)


    def get_bounding_box(self, col_index: int) -> BoundingBox:
        grid_width = self.grid['width']
        grid_height = self.grid['height']

        col_x = col_index % grid_width
        col_y = floor(col_index / grid_width)

        native_size = self.config.processor.native.size

        pixel_width = native_size.width / grid_width
        pixel_height = native_size.height / grid_height

        x = col_x * pixel_width
        y = col_y * pixel_height

        return BoundingBox(round(x), round(y), round(pixel_width), round(pixel_height))


    def save(self) -> None:
        for variation in self.config.output.targets:
            self.save_variation(variation)


    def save_variation(self, variation: ConfigOutputTarget) -> None:
        resized = self.im.resize((variation.size.width, variation.size.width), resample=Image.LANCZOS)
        effects = self.process_variation_effects(variation, resized)

        out = effects.convert(variation.mode)
        output_path = self.get_output_path()

        os.makedirs(output_path, exist_ok=True)
        out.save(os.path.join(output_path, self.get_variation_filename(variation)))


    def process_variation_effects(self, variation: ConfigOutputTarget, im: Image) -> Image:
        ep = EffectProcessor()

        return ep.process_effects(im, variation.effects)


    def get_variation_filename(self, variation: ConfigOutputTarget):
        return f"{self.id}.{variation.name}.{variation.format}"


    def get_output_path(self) -> str:
        output_depth=self.run_opts.output_depth

        ext_path = os.path.sep.join(str(self.id).zfill(output_depth)[-output_depth:])

        return os.path.join(self.run_opts.output, ext_path)
