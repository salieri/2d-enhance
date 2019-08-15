import random
from PIL import ImageDraw, Image, ImageFont

from config import ConfigContentType
from font_scanner import FontLibrary

class TextProcessor:
    def __init__(self, font_library: FontLibrary):
        self.font_library = font_library

    def process_text(self, content: ConfigContentType, text_im: Image.Image) -> Image.Image:
        font_result = self.font_library.get_random_font()
        font_size = random.randint(content.font_size.min, content.font_size.max)
        font = ImageFont.truetype(self.font_library.get_filename(font_result), font_size)
        draw = ImageDraw.Draw(text_im)
        txt = ''

        for line in range(3):
            txt += ''.join(random.choices(content.characters, k=10)) + "\n"

        (tw, th) = draw.multiline_textsize(txt, font=font)

        draw.multiline_text(
            (round((text_im.width / 2) - (tw / 2)), round((text_im.height / 2) - (th / 2))),
            txt,
            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(128, 255)),
            font=font,
            align='center'
        )

        return text_im


