import random
from typing import Union, List

def select_one(chance_list: List[dict]) -> dict:
    total = sum(c['chance'] for c in chance_list)

    r = random.uniform(0, total)
    acc = 0

    for c in chance_list:
        acc += c['chance']

        if r <= acc:
            return c

    return chance_list[-1]


def select_range(a: float, b: float) -> float:
    return random.uniform(a, b)


def should(obj: dict) -> bool:
    return (random.random() <= obj['chance'])


def get_random_color(solid: Union[bool, tuple, list] = False) -> tuple:
    alpha = 255

    if type(solid) in [list, tuple]:
        alpha = random.randint(solid[0], solid[1])

    if solid is False:
        alpha = 255

    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)
