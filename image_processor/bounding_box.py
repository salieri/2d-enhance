
class BoundingBox:
    x: int
    y: int
    x2: int
    y2: int
    cx: int
    cy: int
    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.x2 = x + width - 1
        self.y2 = y + height - 1
        self.cx = round(x + width / 2)
        self.cy = round(y + height / 2)

