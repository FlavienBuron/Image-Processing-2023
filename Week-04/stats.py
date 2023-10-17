import numpy as np
import os
from PIL import Image

INPUT = "./in/"
OUTPUT = "./out/"


def filter(channel_array, kernel_size, mode=0):
    m,n = channel_array.shape
    d = kernel_size // 2
    filtered_array = np.empty_like(channel_array)
    for i in range(m):
        for j in range(n):
            # Quick and dirty padding. Ignore if out of bound
            i_min = i - d if i - d >= 0 else 0
            i_max = i + d+1 if i + d+1 <= m else m
            j_min = j - d if j - d >= 0 else 0
            j_max = j + d+1 if j + d+1 <= n else n
            if mode == 0:
                filtered_array[i,j] = np.min(channel_array[i_min:i_max, j_min:j_max])
            elif mode == 1:
                filtered_array[i,j] = np.max(channel_array[i_min:i_max, j_min:j_max])
            else:
                min = np.min(channel_array[i_min:i_max, j_min:j_max])
                max = np.max(channel_array[i_min:i_max, j_min:j_max])
                filtered_array[i,j] = max - min
    return filtered_array


if __name__ == "__main__":
    for image in os.listdir(INPUT):
        if not image.startswith("."):
            with Image.open(INPUT+image) as img:
                img_array = np.array(img)
                min3x3 = filter(img_array, 3, 0)
                min5x5 = filter(img_array, 5, 0)
                max3x3 = filter(img_array, 3, 1)
                max5x5 = filter(img_array, 5, 1)
                minmax3x3 = filter(img_array, 3, 2)
                minmax5x5 = filter(img_array, 5, 2)
                img_min3 = Image.fromarray(min3x3)
                img_min5 = Image.fromarray(min5x5)
                img_max3 = Image.fromarray(max3x3)
                img_max5 = Image.fromarray(max5x5)
                img_minmax3 = Image.fromarray(minmax3x3)
                img_minmax5 = Image.fromarray(minmax5x5)
                img_min3.save(OUTPUT + "min3x3_" + image)
                img_min5.save(OUTPUT + "min5x5_" + image)
                img_max3.save(OUTPUT + "max3x3_" + image)
                img_max5.save(OUTPUT + "max5x5_" + image)
                img_minmax3.save(OUTPUT + "min-max3x3_" + image)
                img_minmax5.save(OUTPUT + "min-max5x5_" + image)
    
