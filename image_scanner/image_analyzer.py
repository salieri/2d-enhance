from PIL import Image

class ImageAnalyzer:
    def __init__(self, filename: str):
        self.filename = filename

    def analyze(self) -> dict:
        self.load()

        im = self.im

        (width, height) = im.size

        return {
            'filename': self.filename,
            'width': width,
            'height': height,
            'solid': self.isSolid(im)
        }


    def load(self) -> None:
        self.im = Image.open(self.filename)


    # Check that there are no translucent / transparent pixels
    def isSolid(self, im) -> bool:
        (alphaMin, alphaMax) = im.getchannel('A').getextrema()

        return (alphaMin == alphaMax) and (alphaMax == 255)

