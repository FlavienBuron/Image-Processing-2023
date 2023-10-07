from typing import Tuple
from PIL import Image
import numpy as np
import os

INPUT = "./in/"
OUTPUT = "./out/"


def get_channels(image_array: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Return each color channels from the provided image as an array
    """
    return image_array[:,:,0], image_array[:,:,1], image_array[:,:,2]


def rgb_to_hsl(image_array: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert the input image from RGB to HSL color space.
    Return each individual channels of HSL space.
    """
    r,g,b = get_channels(image_array)
    
    _r = r/255
    _g = g/255
    _b = b/255
    
    cmax = np.maximum.reduce([_r, _g, _b])
    cmin = np.minimum.reduce([_r, _g, _b])

    delta = cmax - cmin
    
    hue = get_hue(_r, _g, _b, cmax, delta)
    lightness = (cmax + cmin) / 2
    saturation = get_saturation(delta, lightness)

    return hue, saturation, lightness


def get_hue(_r: np.ndarray, _g: np.ndarray, _b: np.ndarray,
            cmax: np.ndarray, delta: np.ndarray) -> np.ndarray:

    hue_array = np.empty_like(_r)
    for i in range(_r.shape[0]):
        for j in range(_r.shape[1]):
            if delta[i,j] == 0:
                hue_array[i,j] = 0.0
            elif cmax[i,j] == _r[i,j]:
                hue_array[i,j] = 60 * (((_g[i,j] - _b[i,j])/delta[i,j]) % 6)
            elif cmax[i,j] == _g[i,j]:
                hue_array[i,j] = 60 * (((_b[i,j] - _r[i,j])/delta[i,j]) + 2)
            elif cmax[i,j] == _b[i,j]:
                hue_array[i,j] = 60 * (((_r[i,j] - _g[i,j])/delta[i,j]) + 4)
    return hue_array

def get_saturation(delta: np.ndarray, lightness: np.ndarray) -> np.ndarray:
    saturation_array = np.empty_like(delta)
    for i in range(delta.shape[0]):
        for j in range(delta.shape[1]):
            if delta[i,j] == 0.0:
                saturation_array[i,j] = 0.0
            else:
                saturation_array[i,j] = delta[i,j] / (1 - abs(2*lightness[i,j] -1))
    return saturation_array


def hsl_to_rgb(hue: np.ndarray, saturation: np.ndarray, lightness: np.ndarray):
    rgb = np.empty(shape=(hue.shape[0], hue.shape[1], 3))
    to_rgb = lambda r_, g_, b_, m: ((r_+m)*255, (g_+m)*255, (b_+m)*255)
    for i in range(hue.shape[0]):
        for j in range(hue.shape[1]):
            h = hue[i,j]
            s = saturation[i,j]
            l = lightness[i,j]
            c = (1 - abs(2 * l - 1)) * s
            x = c * (1 - abs((h/60) % 2 - 1))
            m = l - c / 2
            if 0 <= h < 60:
                r, g, b = to_rgb(c,x,0.0,m)
                rgb[i,j] = np.array([r,g,b])
            elif 60 <= h < 120:
                r, g, b = to_rgb(x, c, 0.0, m)
                rgb[i,j] = np.array([r,g,b])
            elif 120 <= h < 180:
                r, g, b = to_rgb(0.0, c, x, m)
                rgb[i,j] = np.array([r,g,b])
            elif 180 <= h < 240:
                r, g, b = to_rgb(0.0, x, c, m)
                rgb[i,j] = np.array([r,g,b])
            elif 240 <= h < 300:
                r, g, b = to_rgb(x, 0.0, c, m)
                rgb[i,j] = np.array([r,g,b])
            else: 
                r, g, b = to_rgb(c, 0.0, x, m)
                rgb[i,j] = np.array([r,g,b])
    return rgb.astype(np.uint8)

if __name__ == "__main__":
    for image in os.listdir(INPUT):
        with Image.open(INPUT+image) as img:
            img_array = np.array(img)
            r,g,b = get_channels(img_array)
            img_r = Image.fromarray(r)
            img_g = Image.fromarray(g)
            img_b = Image.fromarray(b)
            # Showing each channels as grey scales
            # img_r.show()
            # img_g.show()
            # img_b.show()
            h, s, l = rgb_to_hsl(img_array)
            rgb = hsl_to_rgb(h,s,l)
            rgb_img = Image.fromarray(rgb, mode="RGB")
            rgb_img.show()
