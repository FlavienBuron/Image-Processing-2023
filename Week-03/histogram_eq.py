from PIL import Image
import numpy as np
import os

from color_sep_rep import get_channels, rgb_to_hsl, hsl_to_rgb

INPUT = "./in/"
OUTPUT = "./out/"


def equalize_channel(channel_array: np.ndarray, value_range: int) -> np.ndarray:
    """
    Equalize the given channel. The histogram is constructed and equilized
    """
    max = value_range
    nb_bins = value_range + 1
    nb_col = value_range - 1
    if value_range == 1 or value_range == 100:
        max = 100
        nb_bins = 101
        nb_col = 99
        channel_array = np.round(channel_array*(max-1)).astype(np.uint8)
    width, height = channel_array.shape
    size = width * height
    hist, _ = np.histogram(channel_array.flatten(), bins=np.linspace(0,max,nb_bins))
    # hist = np.bincount(inverse)
    cdf = np.cumsum(a=hist)
    cdf_min = np.min(cdf)
    eq = np.empty_like(channel_array)
    for i, col in enumerate(channel_array):
        for j, val in enumerate(col):
            h = round(((cdf[val] - cdf_min) / (size - cdf_min)) * nb_col)
            eq[i,j] = h
    if value_range == 1 or value_range == 100:
        eq = eq / 99
    return eq      


def equalize_rgb(image_array: np.ndarray) -> np.ndarray:
    """
    Equalize the R, G and B channels of the given image
    """
    r,g,b = get_channels(image_array)
    eq_r = equalize_channel(r, 256)
    eq_g = equalize_channel(g, 256)
    eq_b = equalize_channel(b, 256)
    eq_array = np.array([eq_r, eq_g, eq_b])
    eq_array = eq_array.transpose((1,2,0))

    return eq_array


def equalize_lightness(image_array: np.ndarray) -> np.ndarray:
    """
    Equalize the lightness/intensity channel of the given RGB image.
    First convert to HSL then back to RGB after equalization
    """
    h,s,l = rgb_to_hsl(image_array)
    eq_l = equalize_channel(l, 1)
    eq_array = hsl_to_rgb(h, s, eq_l)

    return eq_array


if __name__ == "__main__":
    for image in os.listdir(INPUT):
        with Image.open(INPUT+image) as img:
            img_array = np.array(img)
            if img_array.ndim == 2:
                # image is grey scale
                print(f"Equalizing greyscale image {image}")
                eq = equalize_channel(img_array, 256)
                eq_img = Image.fromarray(eq, mode="L")
                eq_img.save(OUTPUT + "geq_" + image)
            else:
                # image is in color
                print(f"Equalizing RGB channels of image {image}")
                eq = equalize_rgb(img_array)
                eq_img = Image.fromarray(eq, mode="RGB")
                eq_img.save(OUTPUT + "rgb-eq_" + image)
                print(f"Equalizing L channel of image {image}")
                eq2 = equalize_lightness(img_array)
                eq2_img = Image.fromarray(eq2, mode="RGB")
                eq2_img.save(OUTPUT + "hsl-eq_" + image)
