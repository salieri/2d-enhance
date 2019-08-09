from PIL import Image

import util


def grayscale_effect(im, effect):
    return im.convert(mode='L').convert(mode='RGBA')


def reduce_colors_effect(im, effect):
    color_count = util.select_one(effect['colors'])['count']
    return im.convert(mode='P', colors=color_count).convert(mode='RGBA')


def rotate_effect(im, effect):
    angle = util.select_range(effect['angle']['min'], effect['angle']['max'])
    return im.rotate(angle, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))


def translucency_effect(im, effect):
    alpha = util.select_range(effect['alpha']['min'], effect['alpha']['max'])

    lut = map(lambda x: max(0, min(255, round(x * alpha))), range(256))

    return im.putalpha(im.getchannel('A').point(lut))


supported_effects = {
    'grayscale': grayscale_effect,
    'reduce_colors': reduce_colors_effect,
    'rotate': rotate_effect,
    'translucency': translucency_effect
}


class EffectProcessor:
    def process_effects(self, im, effects):
        for effect in effects:
            if util.should(effect) is True:
                im = supported_effects[effect['type']](im, effect)

        return im
