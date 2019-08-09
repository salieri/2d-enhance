import random

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


def should(obj):
    return (random.random() <= obj.chance)

