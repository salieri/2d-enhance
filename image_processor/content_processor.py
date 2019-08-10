from typing import List

import util
from PIL import Image, ImageDraw

from config import ConfigContentType

from .bounding_box import BoundingBox
from .effect_processor import EffectProcessor
from .text_procecssor import TextProcessor
from .shape_processor import ShapeProcessor

from font_scanner import FontLibrary
from image_scanner import ImageLibrary


def sprite_content(content: ConfigContentType, box: BoundingBox, im_library: ImageLibrary, font_library: FontLibrary) -> Image.Image:
    sprite = im_library.get_random_sprite()
    sprite_im = Image.open(sprite.filename).convert('RGBA')

    return sprite_im


def shape_content(content: ConfigContentType, box: BoundingBox, im_library: ImageLibrary, font_library: FontLibrary) -> Image.Image:
    shape_im = Image.new('RGBA', (box.width, box.height), (0, 0, 0, 0))
    sp = ShapeProcessor()

    return sp.process_shape(content.shapes, shape_im)


def text_content(content: ConfigContentType, box: BoundingBox, im_library: ImageLibrary, font_library: FontLibrary) -> Image.Image:
    text_im = Image.new('RGBA', (box.width, box.height), (0, 0, 0, 0))
    tp = TextProcessor(font_library)

    return tp.process_text(content, text_im)


supported_content = {
    'sprite': sprite_content,
    'shape': shape_content,
    'text': text_content
}


class ContentProcessor:
    im: Image
    im_library: ImageLibrary
    font_library: FontLibrary
    bounding_box: BoundingBox

    def __init__(self, im: Image, im_library: ImageLibrary, font_library: FontLibrary, bounding_box: BoundingBox):
        self.im = im
        self.im_library = im_library
        self.font_library = font_library
        self.bounding_box = bounding_box


    def process_content(self, contents: List[ConfigContentType]) -> None:
        for content in contents:
            if util.should(content.chance) is True:
                content_im = supported_content[content.type](self, content)

                self.draw_content(content, content_im)


    def draw_content(self, content: ConfigContentType, content_im: Image.Image) -> None:
        ep = EffectProcessor()
        content_im = ep.process_effects(content_im, content.effects)
        box = self.bounding_box
        mask_im = None

        if util.should(content.draw_chances.clipping) is True:
            mask_im = self.im.getchannel('A')
            mask_dr = ImageDraw.Draw(mask_im)

            mask_dr.rectangle([(0, 0), (mask_im.width - 1, mask_im.height - 1)])
            mask_dr.rectangle([(box.x, box.y), (box.x2, box.y2)])

        if util.should(content.draw_chances.resize) is True:
            fit_mode = 'contain'
        else:
            fit_mode = content.fit

        pos = util.determine_image_position(fit_mode, content_im.width, content_im.height, box.width, box.height)
        resized = content_im.resize((pos[2], pos[3]), resample=Image.LANCZOS)

        self.im.paste(resized, box=(pos[0], pos[1]), mask=mask_im)

