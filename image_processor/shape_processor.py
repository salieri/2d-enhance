from typing import List

from PIL import Image, ImageDraw
import random
import aggdraw

import util

from config import ConfigContentTypeShape

# https://aggdraw.readthedocs.io/en/latest/index.html#aggdraw.Draw
# http://effbot.org/zone/wck-3.htm#introducing

def draw_polygon(point_count: int, shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    coords = []

    for i in range(point_count):
        coords.append(random.randint(0, im.width - 1))
        coords.append(random.randint(0, im.height - 1))

    draw = aggdraw.Draw(im)

    pen = aggdraw.Pen(util.get_random_color(), random.randint(0, 8))
    brush = aggdraw.Brush(util.get_random_color())

    draw.polygon(tuple(coords), pen, brush)

    draw.flush()

    return im


def triangle_shape(shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    return draw_polygon(3, shape, im)


def hexagon_shape(shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    return draw_polygon(6, shape, im)


def ellipse_shape(shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    w = random.randint(10, max(10, im.width - 11))
    h = random.randint(10, max(10, im.height - 11))
    px = random.randint(0, round(im.width / 2))
    py = random.randint(0, round(im.height / 2))

    draw = aggdraw.Draw(im)

    pen = aggdraw.Pen(util.get_random_color(), random.randint(0, 8))
    brush = aggdraw.Brush(util.get_random_color())

    draw.ellipse((px, py, px + w, py + w), pen, brush)

    draw.flush()

    # draw.ellipse([(px, py), (px + w), (py + w)], fill=color, outline=outline, width=width)

    return im


def line_shape(shape: ConfigContentTypeShape, im: Image.Image) -> Image.Image:
    nodes = random.randint(2, 8)
    coords = []

    for i in range(nodes):
        coords.append((random.randint(0, im.width - 1), random.randint(0, im.height - 1)))

    color = util.get_random_color()
    width = random.randint(0, 8)

    draw = aggdraw.Draw(im)
    pen = aggdraw.Pen(color, width)

    m = 0

    while m < (nodes - 1):
        print((coords[m][0], coords[m][1], coords[m+1][0], coords[m+1][1]))
        draw.line((coords[m][0], coords[m][1], coords[m+1][0], coords[m+1][1]), pen)
        m += 1

    print('M', m)
    print('nodes', nodes)
    print('Brush', width)
    print('Color', color)

    # draw = ImageDraw.Draw(im)
    # draw = ImageDraw.Draw(im)
    # draw.line(coords, fill=color, width=width)

    draw.flush()

    return im


supported_shapes = {
    'triangle': triangle_shape,
    'hexagon': hexagon_shape,
    'ellipse': ellipse_shape,
    'line': line_shape
}

class ShapeProcessor:
    def __init__(self):
        pass

    def process_shape(self, shapes: List[ConfigContentTypeShape], im: Image.Image) -> Image.Image:
        for shape in shapes:
            if util.should(shape.chance) is True:
                im = supported_shapes[shape.type](shape, im)

        return im

