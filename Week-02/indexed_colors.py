from PIL import Image
import numpy as np
import os

INPUT = "./in/"
OUTPUT = "./out/"


def create_universal_table():
    """
    Create a universal color table. 
    The values are spread uniformly over the possible range
    """
    color_array = np.linspace(start = 0, stop = 255, num = 6)

    table = {
        0: color_array,
        1: color_array,
        2: color_array,
    }
    
    save_table(table, "universal_table.png")
    print("Created Universal Table")

    return table


def create_adaptive_table(image: np.ndarray, name: str):
    """
    Create a adaptive color table, based on the distribution
    color values in the image
    """
    color_arrays = {
        0: np.empty(shape=(6,)),
        1: np.empty(shape=(6,)),
        2: np.empty(shape=(6,)),
    }

    for i in range(3):
        layer = image[:, :, i].flatten()
        mean = layer.mean().round()
        std = layer.std().round()
        start = mean - 2 * std
        stop = mean + 2 * std
        
        if start < 0 :
            start = 0
        if stop > 255:
            stop = 255
        
        color_arrays[i] = np.linspace(start=start, stop=stop, num=6, dtype=np.uint8)
    save_table(color_arrays, "adaptive_table_" + name)
    print(f"Create Adaptive Table for image {name}")
    
    return color_arrays


def save_table(table_dict, name: str):
    """
    Turns the color table into an RGB image to be saved
    """
    table_array = [[[r, g, b]] 
        for r in table_dict[0]
        for g in table_dict[1] 
        for b in table_dict[2]
    ]
    table_array = np.array(table_array, dtype=np.uint8)
    table_array = table_array.reshape((36, -1, 3))
    table_img = Image.fromarray(table_array, mode='RGB').resize((720, 1080))
    table_img.save(OUTPUT + name)


def find_closest(color_array, pixel_value):
    """
    Find the color in the color array that is the closest to the pixel value
    """
    min_d = 999
    min_idx = 0
    for i, val in enumerate(color_array):
        d = abs(int(val) - int(pixel_value))
        if d < min_d:
            min_d = d
            min_idx = i

    return color_array[min_idx]


def convert_image(image: np.ndarray, color_table):
    new_img = np.empty_like(image)
    for i, col in enumerate(image):
        for j, px in enumerate(col):
            px_r, px_g, px_b = px
            new_px = [
                find_closest(color_table[0], px_r),
                find_closest(color_table[1], px_g),
                find_closest(color_table[2], px_b)
            ]
            new_img[i, j] = np.array(new_px)
    return new_img


if __name__ == "__main__":
    univ_table = create_universal_table()
    for image in os.listdir(INPUT):
        with Image.open(INPUT+image) as img:
            img_array = np.array(img)
            adaptive_table = create_adaptive_table(img_array, image)
            print(f"Converting {image} using Universal Table")
            out_univ = convert_image(img_array, univ_table)
            print(f"Converting {image} using Universal Table")
            out_adapt = convert_image(img_array, adaptive_table)
            conv_univ = Image.fromarray(out_univ)
            conv_adapt = Image.fromarray(out_adapt)
            conv_univ.save(OUTPUT + "universal_" + image)
            conv_adapt.save(OUTPUT + "adaptive_" + image)

