import random
from typing import Union, List

def select_one(chance_list: List):
    total = sum(c.chance for c in chance_list)

    r = random.uniform(0, total)
    acc = 0

    for c in chance_list:
        acc += c.chance

        if r <= acc:
            return c

    return chance_list[-1]


def select_range(a: float, b: float) -> float:
    return random.uniform(a, b)


def should(chance: float) -> bool:
    return random.random() <= chance


def get_random_color(solid: Union[bool, tuple, list] = False) -> tuple:
    alpha = 255

    if type(solid) in [list, tuple]:
        alpha = random.randint(solid[0], solid[1])
    elif solid is False:
        alpha = random.randint(128, 255)

    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha


def determine_image_position(fit: str, src_width: int, src_height: int, target_width: int, target_height: int) -> tuple:
    wd = src_width / target_width
    hd = src_height / target_height

    # if fit == 'clip', just clip it to fit
    d = 1

    if fit == 'cover':
        # some must be seen
        d = min(wd, hd)
    elif fit == 'contain':
        # all must be seen
        d = max(wd, hd)

    nw = min(src_width, src_width / d)
    nh = min(src_height, src_height / d)

    sw = round(target_width - nw)
    sh = round(target_height - nh)

    nx = random.randint(min(0, sw), max(0, sw))
    ny = random.randint(min(0, sh), max(0, sh))

    return (
        nx,
        ny,
        round(nw),
        round(nh)
    )
