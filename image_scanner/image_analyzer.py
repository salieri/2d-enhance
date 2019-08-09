from PIL import Image

class ImageAnalyzer:
    def __init__(self, filename):
        self.filename = filename

    def analyze(self):
        self.load()

        im = self.im

        (width, height) = im.size

        return {
            'filename': self.filename,
            'width': width,
            'height': height,
            'solid': self.isSolid(im)
        }


    def load(self):
        self.im = Image.open(self.filename)


    # Check that there are no translucent / transparent pixels
    def isSolid(self, im):
        (alphaMin, alphaMax) = im.getchannel('A').getextrema()

        return (alphaMin == alphaMax) and (alphaMax == 255)

