from PIL import Image
import numpy as np
from sprite import Sprite
from spriteutil import find_most_common_color


def image_segmentation(rows, cols, image_map, label_map, connect, background):
    label = 1
    for x in range(rows):
        for y in range(cols):
            if np.array_equal(image_map[x][y], background):
                continue
            for i, j in [[x, y-1], [x-1, y-1], [x-1, y], [x-1, y]]:
                if (i, j) < (0, 0) or (i, j) > (rows, cols):
                    continue
                if label_map[i][j] != 0:
                    if label_map[x][y] == 0:
                        label_map[x][y] = label_map[i][j]
                    elif label_map[x][y] != label_map[i][j]:
                        connect[label_map[i][j]].append(label_map[x][y])
                        break
            else:
                if not label_map[x][y]:
                    label_map[x][y] = label
                    connect[label] = []
                    label += 1
    return True


def filter_segmentation(connect, list_key_connect):
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


def combine_segmentation(connect, list_key_connect):
    for index1, key in enumerate(list_key_connect[:-1]):
        for _, key2 in enumerate(list_key_connect[index1+1:], index1+1):
            new_list = connect[key2] + [key2]
            if any(x in connect[key] for x in new_list):
                connect[key] += new_list
                connect[key] = list(set(connect[key]))
                connect[key2].clear()

    return {k: v for k, v in connect.items() if v}


def find_sprites(image, background=None):
    image_map = np.asarray(image)
    rows, cols = image_map.shape[:2]
    label_map = np.zeros((rows, cols), dtype=np.int64)
    connect = {}

    if not background:
        if 'A' in image.mode:
            background = (0, 0, 0, 0)
        else:
            background = find_most_common_color(image)

    image_segmentation(rows, cols, image_map, label_map, connect, background)
    list_key_connect = list(connect.keys())

    filter_segmentation(connect, list_key_connect)
    connect = combine_segmentation(connect, list_key_connect)

    sprites = {}

    for label, x in enumerate(connect, 1):
        for a in connect[x]:
            label_map[label_map == a] = label
        label_map[label_map == x] = label

        temp_array = np.argwhere(label_map == label)
        x_max, y_max = np.amax(temp_array, axis=0)
        x_min, y_min = np.amin(temp_array, axis=0)
        sprites[label] = Sprite(label, x_min.item(), y_min.item(), x_max.item(), y_max.item())

    return sprites, label_map


if __name__ == '__main__':
    image = Image.open('image/optimized_sprite_sheet.png')
    sprites, label_map = find_sprites(image)
    print(len(sprites))
    for label, sprite in sprites.items():
        print(f"Sprite ({label}): [{sprite.top_left}, {sprite.bottom_right}] {sprite.width}x{sprite.height}")