from PIL import Image
import numpy as np
from pprint import pprint
from json import dumps


im = Image.open('im.png')
array = np.asarray(im)
rows, cols = array.shape[:2]
new_array = np.zeros((rows, cols), dtype=np.int64)

label = 1
connect = {}
for x in range(rows):
    for y in range(cols):
        if np.array_equal(array[x][y], [0, 0, 0, 0]):
            continue
        for i, j in [[x, y-1], [x-1, y-1], [x-1, y], [x-1, y]]:
            if (i, j) < (0, 0) or (i, j) > (rows, cols):
                continue
            if new_array[i][j] != 0:
                if new_array[x][y] == 0:
                    new_array[x][y] = new_array[i][j]
                elif new_array[x][y] != new_array[i][j]:
                    connect[new_array[i][j]].append(new_array[x][y])
        if not new_array[x][y]:
            new_array[x][y] = label
            connect[label] = []
            label += 1

temp_list = list(connect.keys())

for x in reversed(temp_list):
    count = 0
    try:
        connect[x] = list(set(connect[x]))
        while True:
            connect[x] += connect[connect[x][count]]
            connect[x] = list(set(connect[x]))
            del connect[connect[x][count]]
            count += 1
    except (IndexError, KeyError):
        continue


temp_list = list(connect.keys())

f = open('obj.js', 'w')
f.write(str(connect))
f.close()

for index1, key in enumerate(temp_list[:-1]):
    for index2, key2 in enumerate(temp_list[index1+1:], index1+1):
        # print(index2, key2)
        new_list = connect[key2] + [key2]
        if any(x in connect[key] for x in new_list):
            connect[key] += new_list
            connect[key] = list(set(connect[key]))
            connect[key2].clear()

connect = {k: v for k, v in connect.items() if v}



for label, x in enumerate(connect, 1):
    for a in connect[x]:
        new_array[new_array == a] = label
    new_array[new_array == x] = label

# np.savetxt("filename", new_array, newline="\n", fmt='%d')