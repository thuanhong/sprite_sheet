from PIL import Image, ImageDraw
import numpy as np


class Sprite:
    def __init__(self, label, x1, y1, x2, y2):
        if any(not isinstance(x, int) or x < 0 for x in [x1, x2, y1, y2]) or (x2, y2) <= (x1, y1):
            raise ValueError('Invalid coordinates')
        self._label = label
        self._top_left = (x1, y1)
        self._bottom_right = (x2, y2)
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


class SpriteSheet:
    def __init__(self, fd, background=None):
        self.fd = self.__image_obj(fd)
        if background:
            self._background_color = background
        else:
            self._background_color = SpriteSheet.find_most_common_color(self.fd)
        self.__label_map = ''
        self.__sprites = ''
    
    @property
    def background_color(self):
        return self._background_color

    @staticmethod
    def find_most_common_color(image):
        """
        Get the pixel color that is the most used in this image
        @param image : a Image object
        @return : most common color in image
        """
        # Get colors from image object
        pixels = image.getcolors(image.width * image.height)
        # Get the most frequent color
        most_common_color = max(pixels, key=lambda t: t[0])
        return most_common_color[1]
    
    def __image_obj(self, fd):
        try:
            return Image.open(fd)
        except UnicodeDecodeError:
            return Image.open(fd.name)
    
    def __convert_pixels_to_label_map(self, rows, cols, image_map, label_map, connect):
        """
        convert pixel to label follow blob detect algorithm
        @param rows : width image
        @param cols : height image
        @param image_map : numpy array 3d object that references image
        """
        label = 1
        for x in range(rows):
            for y in range(cols):
                if np.array_equal(image_map[x][y], self._background_color):
                    continue
                # check 4 neighborhood left, top left, top, top right
                for i, j in [[x, y-1], [x-1, y-1], [x-1, y], [x-1, y]]:
                    # check index out range array
                    if (i, j) < (0, 0) or (i, j) > (rows, cols):
                        continue
                    # connect neighborhood label with current label if possible
                    if label_map[i][j] != 0:
                        if label_map[x][y] == 0:
                            label_map[x][y] = label_map[i][j]
                        elif label_map[x][y] != label_map[i][j]:
                            connect[label_map[i][j]].append(label_map[x][y])
                            break
                else:
                    # assign current position is new label
                    if not label_map[x][y]:
                        label_map[x][y] = label
                        connect[label] = []
                        label += 1
        return True

    def __connect_segmentation(self, connect, list_key_connect):
        """
        connect label like:
        connect = {             connect = {
            1: {2,3,4}              1 : {2,3,4,5,6,7,8,9}
            2: {5,6}        =>  }
            3: {7,8,9}
        }
        @param connect : dict contain all pixels label and sprite's label that key belong to
        @param list_key_connect : list contain all key label in dict connect
        """
        for x in reversed(list_key_connect):
            count = 0
            try:
                connect[x] = list(set(connect[x]))
                while count < len(connect[x]):
                    connect[x] += connect[connect[x][count]]
                    connect[x] = list(set(connect[x]))
                    count += 1
            except (IndexError):
                continue
        return True


    def __combine_labels(self, connect, list_key_connect):
        """
        combine labels with the same connection
        @param connect : dict contain all pixels label and sprite's label that key belong to
        @param list_key_connect : list contain all key label in dict connect
        @return a dict contain label and sprite's label that key belong to
        """
        for index1, key in enumerate(list_key_connect[:-1]):
            for _, key2 in enumerate(list_key_connect[index1+1:], index1+1):
                new_list = connect[key2] + [key2]
                if any(x in connect[key] for x in new_list):
                    connect[key] += new_list
                    connect[key] = list(set(connect[key]))
                    connect[key2].clear()

        return {k: v for k, v in connect.items() if v}
        
    def find_sprites(self):
        """ 
        Detect sprites inside the image
        Return a 2D label map and a dict that stores:
                key: sprite's label
                value: its Sprite's object
        """
        image_map = np.asarray(self.fd)
        rows, cols = image_map.shape[:2]
        label_map = np.zeros((rows, cols), dtype=np.int64)
        connect = {}

        self.__convert_pixels_to_label_map(rows, cols, image_map, label_map, connect)
        list_key_connect = list(connect.keys())

        # connect labels by sprite's label that key belong to
        self.__connect_segmentation(connect, list_key_connect)
        # combine labels with the same connection
        connect = self.__combine_labels(connect, list_key_connect)

        sprites = {}
        
        for label, x in enumerate(connect, 1):
            for a in connect[x]:
                label_map[label_map == a] = label
            label_map[label_map == x] = label

            temp_array = np.argwhere(label_map == label)
            y_max, x_max = np.amax(temp_array, axis=0)
            y_min, x_min = np.amin(temp_array, axis=0)
            sprites[label] = Sprite(label, x_min.item(), y_min.item(), x_max.item(), y_max.item())

        self.__sprites, self.__label_map = sprites, label_map
        return sprites, label_map.tolist()

    def create_sprite_labels_image(self):
        """
        Draws the masks of the sprites at the exact same position that the sprites were in the original image.
        Returns an image of equal dimension (width and height) as the original image that was passed to the function
        """
        if self.__label_map == '':
            self.find_sprites()
        label_map = self.__label_map

        # random color base on mode color (RGBA/RGB)
        mode_color, c = ('tuple(np.random.randint(256, size=3)) + (255,)', 3) if len(self._background_color) == 4 else ('tuple(np.random.randint(256, size=3))', 2)
        color = {}
        color[0] = self._background_color

        # convert label map (2d) to array image (3d) [[0,0,0,1,1,1,0], ... [1,0,0,1,1,1,0]] -> [[[0,0,0], [0,0,0]] ... [[1,0,0], [0,0,0]]]
        zeros_array = np.zeros((*label_map.shape, c), dtype=int)
        label_map = np.expand_dims(label_map, axis=2)
        label_map = np.append(label_map, zeros_array, axis=2)

        # replace label by color in dict color
        coordinate = np.argwhere(np.all(label_map == [0, *[0]*c], axis=2))
        for x, y in coordinate:
            label_map[x][y] = color[0]

        for x in self.__sprites.keys():
            color[x] = eval(mode_color)
            coordinate = np.argwhere(np.all(label_map == [x, *[0]*c], axis=2))
            for i, j in coordinate:
                label_map[i][j] = color[x]

        # draws a rectangle (bounding box) around each sprite mask, of the same color used for drawing the sprite mask
        new_image = Image.fromarray(label_map.astype('uint8'))
        draw = ImageDraw.Draw(new_image)
        for x, y in self.__sprites.items():
            draw.rectangle((y.top_left, y.bottom_right), outline=color[x])

        return new_image


if __name__ == '__main__':
    obj = SpriteSheet('im.png')
    obj.create_sprite_labels_image().save('new.png')