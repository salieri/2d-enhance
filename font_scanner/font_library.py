import itertools as it, glob
import os
import json
from typing import Iterable, List
import random
import marshmallow.validate

from PIL import ImageFont
from datetime import datetime
from dataclasses import field
from marshmallow_dataclass import dataclass


from config import Config

MAGIC = 'tartarus-generator.font-scan-cache'
VERSION = '0.1.0'

@dataclass
class FontAnalysisResult:
    filename: str = field()

@dataclass
class FontLibraryData:
    scan_date: str
    type: str = field(metadata={'validate': marshmallow.validate.Equal(MAGIC)}, default=MAGIC)
    version: str = field(default=VERSION)
    fonts: List[FontAnalysisResult] = field(default_factory=lambda: [])

class FontLibrary:
    config: Config
    base_path: str
    file_extensions: List[str]
    data: FontLibraryData

    def __init__(self, config: Config, base_path: str):
        self.config = config
        self.base_path = base_path
        self.file_extensions = ['*.oft', '*.ttf']


    def scan_filenames(self) -> Iterable:
        return it.chain.from_iterable(glob.iglob(os.path.join(self.base_path, '**', ext), recursive=True) for ext in self.file_extensions)


    def scan(self) -> FontLibraryData:
        fonts = []

        for filename in self.scan_filenames():
            try:
                fn = os.path.relpath(filename, self.base_path)
                (result, font_err) = FontAnalysisResult.Schema().load({'filename': fn})

                fonts.append(FontAnalysisResult.Schema().dump(result)[0])
                #
                #
                # ff = {
                #     "variations": []
                # }
                #
                # for size in [9, 10, 12, 14, 18, 24, 32, 48]:
                #     ff['variations'].append(ImageFont.truetype(filename, size=size))
                #
                # (family, style) = ff['variations'][0].getname()
                # ff['name'] = f"{family}-{style}"
                #
                # fonts.append(ff)
            except OSError as e:
                print(f"Failed loading '{filename}' -- {e}")

        (self.data, err) = FontLibraryData.Schema().load(
            {
                'type': MAGIC,
                'version': VERSION,
                'scan_date': str(datetime.now()),
                'fonts': fonts
            }
        )

        return self.data


    def get_random_font(self) -> FontAnalysisResult:
        return random.choice(self.data.fonts)


    def load(self, filename: str) -> FontLibraryData:
        with open(filename, 'r') as fp:
            (data, err) = FontLibraryData.Schema().load(json.load(fp))

            if bool(err) is True:
                print(err)
                raise Exception(f"Invalid data in '{filename}'")

            self.data = data

            return data


    def save(self, filename: str) -> None:
        with open(filename, 'w') as fp:
            (data, err) = FontLibraryData.Schema().dump(self.data)
            json.dump(data, fp)


    def get_filename(self, far: FontAnalysisResult) -> str:
        return os.path.join(self.base_path, far.filename)
