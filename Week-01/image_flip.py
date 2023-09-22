from PIL import Image
import numpy as np
import os
import argparse

INPUT = "./in/"
OUTPUT = "./out/"

parser = argparse.ArgumentParser()
parser.add_argument(
    '--orient', 
                    type=str,
                    default='all',
                    help="[h]orizontal, [v]ertical, both, all (default)")
args = parser.parse_args()

def horizontal_flip(image_array: np.ndarray):
    """
    Process the image to be flipped horizontally (vertical axis)
    """
    new_image = np.empty_like(image_array)
    for i, row in enumerate(image_array):
        # for each rows of the 3d matrix, reverse the order
        # Equivalent to iterating through the whole array in reverse order
        # and placing them in a new array
        new_image[i] = row[::-1]
    return new_image
    

def vertical_flip(image_array: np.ndarray):
    """
    Procees the image to be flipped vertically (horizontal axis)
    """
    new_image = np.empty_like(image_array)
    # Transpose the array such that the previously used technique
    # can work on the columns instead of rows
    for i, row in enumerate(np.transpose(image_array, (1, 0, 2))):
        new_image[i] = row[::-1]
    # transpose the array back to original orientation
    return np.transpose(new_image, (1, 0, 2)) 

def double_flip(image_array: np.ndarray):
    """
    Process the image to be flipped both vertically and horizontally
    """
    # first flip the image horizontally
    h_flip = horizontal_flip(image_array)
    # then flip vertically
    v_flip = vertical_flip(h_flip)
    return v_flip

for image in os.listdir(INPUT):
    with Image.open(INPUT + image) as img:
        img_array = np.array(img)
        if args.orient == 'h':
            out = horizontal_flip(img_array)
            flip = Image.fromarray(out)
            flip.save(OUTPUT + 'h_' + image)
        if args.orient == 'v':
            out = vertical_flip(img_array)
            flip = Image.fromarray(out)
            flip.save(OUTPUT + 'v_' + image)
        if args.orient == "both":
            out = double_flip(img_array)
            flip = Image.fromarray(out)
            flip.save(OUTPUT + "vh_" + image)
        if args.orient == "all":
            out = horizontal_flip(img_array)
            flip = Image.fromarray(out)
            flip.save(OUTPUT + 'h_' + image)
            out = vertical_flip(img_array)
            flip = Image.fromarray(out)
            flip.save(OUTPUT + 'v_' + image)
            out = double_flip(img_array)
            flip = Image.fromarray(out)
            flip.save(OUTPUT + "vh_" + image)

