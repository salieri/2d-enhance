from PIL import Image
import hashlib

from marshmallow_dataclass import dataclass

@dataclass
class ImageAnalysisResult:
    filename: str
    width: int
    height: int
    md5: str
    solid: bool


class ImageAnalyzer:
    im: Image.Image

    def __init__(self, filename: str):
        self.filename = filename


    def analyze(self) -> ImageAnalysisResult:
        self.load()

        im = self.im

        (width, height) = im.size

        return ImageAnalysisResult.Schema.Load(
            {
                'filename': self.filename,
                'width': width,
                'height': height,
                'md5': self.get_md5(self.filename),
                'solid': self.is_solid(im)
            }
        )


    def load(self) -> None:
        self.im = Image.open(self.filename)


    # Check that there are no translucent / transparent pixels
    def is_solid(self, im: Image.Image) -> bool:
        (alphaMin, alphaMax) = im.getchannel('A').getextrema()

        return (alphaMin == alphaMax) and (alphaMax == 255)


    def get_md5(self, filename:str) -> str:
        with open(filename) as fp:
            data = fp.read()
            return hashlib.md5(data).hexdigest()
