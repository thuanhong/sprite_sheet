from find_sprite import find_sprites
from PIL import Image, ImageDraw
import numpy as np


def create_sprite_labels_image(sprites, label_map, background=(255, 255, 255)):
    mode_color, c = ('tuple(np.random.randint(256, size=3)) + (255,)', 3) if len(background) == 4 else ('tuple(np.random.randint(256, size=3))', 2)
    color = {}
    color[0] = background
    zeros_array = np.zeros((*label_map.shape, c), dtype=int)
    label_map = np.expand_dims(label_map, axis=2)
    label_map = np.append(label_map, zeros_array, axis=2)

    coordinate = np.argwhere(np.all(label_map == [0, *[0]*c], axis=2))
    for x, y in coordinate:
        label_map[x][y] = color[0]

    for x in sprites.keys():
        color[x] = eval(mode_color)
        coordinate = np.argwhere(np.all(label_map == [x, *[0]*c], axis=2))
        for i, j in coordinate:
            label_map[i][j] = color[x]

    
    im = Image.fromarray(label_map.astype('uint8'))
    draw = ImageDraw.Draw(im)
    for x, y in sprites.items():
        draw.rectangle((y.top_left, y.bottom_right), outline=color[x])

    return im



if __name__ == '__main__':
    image = Image.open('im.png')
    sprites, label_map = find_sprites(image)
    sprite_label_image = create_sprite_labels_image(sprites, label_map)
    sprite_label_image.save('round.png')