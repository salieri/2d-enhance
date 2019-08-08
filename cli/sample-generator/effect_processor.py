import random
from PIL import Image


def select_one(chance_list):
    total = sum(c['chance'] for c in chance_list)

    r = random.uniform(0, total)
    acc = 0

    for c in chance_list:
        acc += c['chance']

        if r <= acc:
            return c

    return chance_list[-1]


def select_range(a, b):
    return random.uniform(a, b)


def grayscale_effect(im, effect):
    return im.convert(mode='L').convert(mode='RGBA')


def reduce_colors_effect(im, effect):
    color_count = select_one(effect['colors'])['count']
    return im.convert(mode='P', colors=color_count).convert(mode='RGBA')


def rotate_effect(im, effect):
    angle = select_range(effect['angle']['min'], effect['angle']['max'])
    return im.rotate(angle, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))


supported_effects = {
    'grayscale': grayscale_effect,
    'reduce_colors': reduce_colors_effect,
    'rotate': rotate_effect
}


class EffectProcessor:
    def process_effects(self, im, effects):
        for effect in effects:
            type = effect['type']

            if type in supported_effects:
                im = supported_effects[type](im, effect)

        return im




