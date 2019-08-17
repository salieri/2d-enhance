from typing import List

from src import util
from PIL import Image

from src.config import ConfigBackgroundType
from .effect_processor import EffectProcessor
from src.image_scanner import ImageLibrary


def bitmap_background(background: ConfigBackgroundType, im_library: ImageLibrary, width: int, height: int) -> Image.Image:
    bg = im_library.get_random_background()
    bg_im = Image.open(im_library.get_filename(bg)).convert('RGBA')
    return bg_im


def bitmap_solid(background: ConfigBackgroundType, im_library: ImageLibrary, width: int, height: int) -> Image.Image:
    color = util.get_random_color(True)
    return Image.new('RGBA', size=(width, height), color=color)


def bitmap_transparent(background: ConfigBackgroundType, im_library: ImageLibrary, width: int, height: int) -> Image.Image:
    return Image.new('RGBA', size=(width, height), color=(0, 0, 0, 0))


def bitmap_gradient(background: ConfigBackgroundType, im_library: ImageLibrary, width: int, height: int) -> Image.Image:
    return bitmap_solid(background, im_library, width, height)


def bitmap_noise(background: ConfigBackgroundType, im_library: ImageLibrary, width: int, height: int) -> Image.Image:
    return bitmap_solid(background, im_library, width, height)


supported_content = {
    'bitmap': bitmap_background,
    'solid': bitmap_solid,
    'transparent': bitmap_transparent,
    'gradient': bitmap_gradient,
    'noise': bitmap_noise
}


class BackgroundProcessor:
    im_library: ImageLibrary
    width: int
    height: int

    def __init__(self, im_library: ImageLibrary, width: int, height: int):
        self.im_library = im_library
        self.width = width
        self.height = height


    def process_background(self, backgrounds: List[ConfigBackgroundType]) -> Image.Image:
        im = Image.new('RGBA', size=(self.width, self.height), color=(0, 0, 0, 0))

        for bg in backgrounds:
            if util.should(bg.chance) is True:
                bg_im = supported_content[bg.type](bg, self.im_library, self.width, self.height)
                im = self.finalize_background(bg, bg_im, im)

        return im


    def finalize_background(self, bg: ConfigBackgroundType, bg_im: Image.Image, im: Image.Image) -> Image.Image:
        ep = EffectProcessor()
        bg_im = ep.process_effects(bg_im, bg.effects)
        pos = util.determine_image_position(bg.fit, bg_im.width, bg_im.height, self.width, self.height)
        resized = bg_im.resize((pos[2], pos[3]), resample=Image.LANCZOS)

        im.paste(resized, box=(pos[0], pos[1]))

        return im

