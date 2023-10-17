import numpy as np
import os
from PIL import Image

INPUT = "./in/"
OUTPUT = "./out/"

laplacian_gaussian = np.array([[0,1,1,1,0],
                               [1,3,0,3,1],
                               [1,0,-24,0,1],
                               [1,3,0,3,1],
                               [0,1,1,1,0]
                               ])

sobel_h = np.array([[-0.25, 0.0, 0.25],
                    [-0.50, 0.0, 0.5],
                    [-0.25, 0.0, 0.25]
                    ])

sobel_v = np.array([[-0.25, -0.50, -0.25],
                    [ 0.00,  0.00,  0.00],
                    [ 0.25,  0.50,  0.25]
                    ])

sobel = (sobel_h, sobel_v)


def log(sigma, x, y):
    a = -(1 / (np.pi * sigma**4))
    b = 1 - ((x**2 + y**2) / (2 * sigma**2))
    c = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return a * b * c


def get_log_kernel(size, sigma):
    k = np.empty(shape=(size, size))
    offset = (size - 1) / 2
    for i in range(size):
        for j in range(size):
            k[i,j] = log(sigma, (i - offset), (j - offset))
    return k


def edge_detection(channel_array, kernel_h, kernel_v = None):
    x, _ = kernel_h.shape
    d = x//2
    with_padding = np.pad(array=channel_array, pad_width=d, mode='edge')
    output = np.empty_like(channel_array)
    for i in range(d,with_padding.shape[0]-2*d):
        for j in range(d, with_padding.shape[1]-2*d):
            s = np.sum(with_padding[i-d:i+d+1, j-d:j+d+1] * kernel_h)
            if kernel_v is not None:
                s1 = np.sum(with_padding[i-d:i+d+1, j-d:j+d+1] * kernel_v)
                s = np.sqrt(np.square(s) + np.square(s1))
            output[i-d, j-d] = s
    return output

if __name__ == "__main__":
    for image in os.listdir(INPUT):
        if not image.startswith("."):
            with Image.open(INPUT+image) as img:
                img_array = np.array(img)
                log = edge_detection(img_array, get_log_kernel(3, 1))
                ed = edge_detection(img_array, *sobel)
                img_log = Image.fromarray(log)
                img_ed = Image.fromarray(ed)
                img_log.save(OUTPUT + "log3x3-1_" + image)
                img_ed.save(OUTPUT + "sobel_" + image)
