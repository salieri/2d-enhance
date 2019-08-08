
class SpriteProcessor:
    def __init__(self, im):
        self.im = im


    def getBoundingBox(self, col_index):
        col_x = col_index % self.im.grid.width
        col_y = col_index / self.im.grid.width

        pixel_width = self.im.size.width / self.im.config.content.grid.width
        pixel_height = self.im.config.processor.native.size.height / self.im.config.content.grid.height

        x = col_x * pixel_width
        y = col_y * pixel_height

        return {
         'x': x,
         'y': y,
         'x2': x + pixel_width - 1,
         'y2': y + pixel_height - 1,
         'cx': round(x + pixel_width / 2),
         'cy': round(y + pixel_height / 2)
        }


    def drawText(self):


    def drawShape(self):


    def drawSprite(self):


    def should(self, chance):
