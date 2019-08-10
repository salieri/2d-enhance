from typing import List

from PIL import Image, ImageDraw
import random

import util

from config import ConfigContentTypeShape


def draw_polygon(point_count: int, shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    outline = None
    color = util.get_random_color()
    draw = ImageDraw.Draw(im)
    coords = []

    for i in range(point_count):
        coords.append(random.randint((0, im.width - 1), random.randint(0, im.height - 1)))

    draw.polygon(coords, fill=color, outline=outline)

    return im


def triangle_shape(shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    return draw_polygon(3, shape, im)


def hexagon_shape(shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    return draw_polygon(6, shape, im)


def oval_shape(shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    w = random.randint(10, max(10, im.width - 11))
    h = random.randint(10, max(10, im.height - 11))
    px = random.randint(0, round(im.width / 2))
    py = random.randint(0, round(im.height / 2))
    color = util.get_random_color()
    outline = util.get_random_color()
    width = random.randint(0, 8)
    draw = ImageDraw.Draw(im)

    draw.ellipse([(px, py), (px + w), (py + w)], fill=color, outline=outline, width=width)

    return im


def line_shape(shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    nodes = random.randint(2, 16)
    coords = []

    for i in range(nodes):
        coords.append((random.randint(0, im.width - 1), random.randint(0, im.height - 1)))

    color = util.get_random_color()
    width = random.randint(0, 8)
    draw = ImageDraw.Draw(im)

    draw.line(coords, fill=color, width=width)

    return im


supported_shapes = {
    'triangle': triangle_shape,
    'hexagon': hexagon_shape,
    'oval': oval_shape,
    'line': line_shape
}

class ShapeProcessor:
    def __init__(self):
        pass


    def process_shape(self, shapes: List[ConfigContentTypeShape], im: Image.Image) -> Image.Image:
        for shape in shapes:
            if util.should(shape.chance) is True:
                im = supported_shapes[shape.type](self, shape, im)

        return im

