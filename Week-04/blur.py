import numpy as np
import os
from PIL import Image

INPUT = "./in/"
OUTPUT = "./out/"


def mean_filter(channel_array, kernel_size):
    m,n = channel_array.shape
    d = kernel_size // 2
    filtered_array = np.empty_like(channel_array)
    for i in range(m):
        for j in range(n):
            # Quick and dirty padding. Ignore if out of bound, same as if there were 0s
            i_min = i - d if i - d >= 0 else 0
            i_max = i + d+1 if i + d+1 <= m else m
            j_min = j - d if j - d >= 0 else 0
            j_max = j + d+1 if j + d+1 <= n else n
            mean = np.mean(channel_array[i_min:i_max, j_min:j_max])
            filtered_array[i,j] = mean
    return filtered_array


if __name__ == "__main__":
    for image in os.listdir(INPUT):
        if not image.startswith("."):
            with Image.open(INPUT+image) as img:
                img_array = np.array(img)
                filtered3x3 = mean_filter(img_array, 3)
                filtered5x5 = mean_filter(img_array, 5)
                filtered9x9 = mean_filter(img_array, 9)
                img_filtered3x3 = Image.fromarray(filtered3x3)
                img_filtered5x5 = Image.fromarray(filtered5x5)
                img_filtered9x9 = Image.fromarray(filtered9x9)
                img_filtered3x3.save(OUTPUT + "mean3x3_" + image)
                img_filtered5x5.save(OUTPUT + "mean5x5_" + image)
                img_filtered9x9.save(OUTPUT + "mean9x9_" + image) 
