from typing import List

from PIL import Image

import util
from config import ConfigEffect


def grayscale_effect(im: Image.Image, effect: ConfigEffect) -> Image.Image:
    return im.convert(mode='L').convert(mode='RGBA')


def reduce_colors_effect(im: Image.Image, effect: ConfigEffect) -> Image.Image:
    color_count = util.select_one(effect.colors).count
    return im.convert(mode='P', colors=color_count).convert(mode='RGBA')


def rotate_effect(im: Image.Image, effect: ConfigEffect) -> Image.Image:
    angle = util.select_range(effect.angle.min, effect.angle.max)
    return im.rotate(angle, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))


def translucency_effect(im: Image.Image, effect: ConfigEffect) -> Image.Image:
    alpha = util.select_range(effect.alpha.min, effect.alpha.max)

    lut = map(lambda x: max(0, min(255, round(x * alpha))), range(256))

    return im.putalpha(im.getchannel('A').point(lut))

# outline

supported_effects = {
    'grayscale': grayscale_effect,
    'reduce_colors': reduce_colors_effect,
    'rotate': rotate_effect,
    'translucency': translucency_effect
}


class EffectProcessor:
    def process_effects(self, im: Image.Image, effects: List[ConfigEffect]) -> Image.Image:
        for effect in effects:
            if util.should(effect.chance) is True:
                im = supported_effects[effect.type](im, effect)

        return im
