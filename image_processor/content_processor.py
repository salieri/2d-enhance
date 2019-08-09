from util import select_one

def sprite_content(cp):
    pass

def shape_content(cp):
    pass

def text_content(cp):
    pass


supported_content = {
    'sprite': sprite_content,
    'shape': shape_content,
    'text': text_content
}


class ContentProcessor:
    def __init__(self, im, content, bounding_box):
        self.im = im
        self.content = content
        self.bounding_box = bounding_box


    def process_content(self):
        # content = select_one(self.config['content']['types'])

        return supported_content[self.content['type']](self)


