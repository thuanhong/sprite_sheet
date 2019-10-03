from PIL import Image
import timeit


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


if __name__ == '__main__':
    image = Image.open('im.png')
    # print(timeit.timeit(stmt=lambda: find_most_common_color(image), number=1))
    print(find_most_common_color(image))