from PIL import Image, ImageFilter
import numpy as np
import timeit


image = Image.open('metal.png')
print(np.asarray(image))
image.filter(ImageFilter.FIND_EDGES).save('1.png')

# arr.save('new.png')

array_position_edge = np.argwhere(np.all(np.asarray(image.filter(ImageFilter.FIND_EDGES)) != [0, 0, 0, 0], axis=2))
# print(array_position_edge.size)
 

# print(open_list[0])
# a = np.where(np.all(array_position_edge == open_list[0], axis=1))
# print(a)
# b = np.where(np.all(array_position_edge == [1, 407], axis=1))
# print(b)

# print(np.append(open_list, array_position_edge[a], axis=0))
count = 1

def test():
    global array_position_edge, count
    while array_position_edge.size:
        open_list = np.expand_dims(array_position_edge[0], axis=0)
        array_position_edge = np.delete(array_position_edge, 0, axis=0)
        close_list = np.array([[-1, -1]])
        while open_list.size:
            x, y = open_list[0]
            list_neighbor = [[x, y-1], [x, y+1], [x+1, y], [x-1, y], [x-1, y-1], [x-1, y+1], [x+1, y-1], [x+1, y+1]]
            for coordinate in list_neighbor:
                index = np.where(np.all(array_position_edge == coordinate, axis=1))[0]
                if index.size:
                    open_list = np.append(open_list, array_position_edge[index], axis=0)
                    array_position_edge = np.delete(array_position_edge, index, axis=0)
            close_list = np.append(close_list, open_list[[0]], axis=0)
            open_list = np.delete(open_list, 0, axis=0)
        print(close_list)
        return


# print(timeit.timeit(stmt=lambda: test(), number=1))