import random
from util import should
from PIL import Image, ImageDraw

from .effect_processor import EffectProcessor

def sprite_content(cp, content):
    sprite = random.choice(cp.im_library['sprites'])
    sprite_im = Image.open(sprite['filename']).convert('RGBA')

    return sprite_im


def shape_content(cp, content):
    box = cp.bounding_box
    shape_im = Image.new('RGBA', (box['width'], box['height']), (0, 0, 0, 0))

    sp = ShapeProcessor()

    return sp.process_shape(content['shapes'], shape_im)


def text_content(cp, content):
    box = cp.bounding_box
    text_im = Image.new('RGBA', (box['width'], box['height']), (0, 0, 0, 0))

    tp = TextProcessor(cp.font_library)

    return tp.process_text(content, text_im)


supported_content = {
    'sprite': sprite_content,
    'shape': shape_content,
    'text': text_content
}


class ContentProcessor:
    def __init__(self, im, im_library, font_library, bounding_box):
        self.im = im
        self.im_library = im_library
        self.font_library = font_library
        self.bounding_box = bounding_box


    def process_content(self, contents):
        for content in contents:
            if should(content) is True:
                content_im = supported_content[content['type']](self)

                self.draw_content(content, content_im)


    def draw_content(self, content, content_im):
        ep = EffectProcessor()
        content_im = ep.process_effects(content_im, content['effects'])
        box = self.bounding_box
        mask_im = None

        if should(content.clipping) is True:
            mask_im = self.im.getchannel('A')
            mask_dr = ImageDraw.Draw(mask_im)

            mask_dr.rectangle([(0, 0), (mask_im.width - 1, mask_im.height - 1)])
            mask_dr.rectangle([(box['x1'], box['y1']), (box['x2'], box['y2'])])

        cx = box['cx'] - round(content_im.width / 2)
        cy = box['cy'] - round(content_im.height / 2)

        self.im.paste(content_im, box=(cx, cy), mask=mask_im)

