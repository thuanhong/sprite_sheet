from PIL import Image


class Sprite():
    def __init__(self, label, x1, y1, x2, y2):
        if any(not isinstance(x, int) or x < 0 for x in [x1, x2, y1, y2]) or (x2, y2) <= (x1, y1):
            raise ValueError('Invalid coordinates')
        self._label = label
        self._top_left = (y1, x1)
        self._bottom_right = (y2, x2)
        self._width = x2 - x1 + 1
        self._height = y2 - y1 + 1

    @property
    def label(self):
        return self._label
    @property
    def top_left(self):
        return self._top_left
    @property
    def bottom_right(self):
        return self._bottom_right
    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height
