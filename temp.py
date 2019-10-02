from PIL import Image, ImageFilter
import numpy as np


image = Image.open('metal.png')

ar = image.filter(ImageFilter.FIND_EDGES)
ar.show()
print(np.argwhere(np.all(np.asarray(image) != [0, 0, 0, 0], axis=2)))