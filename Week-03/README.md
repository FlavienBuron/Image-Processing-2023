## Assigment 3 (Week 3)

This code equalize the histogram of greyscale images (1 channel) and of color images (3 channels, RGB or HSL).

To run the code execute the following command:
```bash
python histogram_eq.py 
```

This will output the following:
* If a greyscale image is provided in the inputs, an equalized greyscale image will be in the outputs
* If a color image is in the inputs, the output will be an image equalized on each RGB channels, and an image equalized on the lightness channel after the image has been converted to HSL color space, then back to RGB after equalization.

Additionaly, the module `color_sep_rep.py` is used by the previous module to separate the different channels, convert images from RGB to HSL color space, and to convert images from HSL to RGB color space.

All images present in the folder `/in/` will be used and outputs are placed in the folder `/out/` with a prefix according to the histogram equalization (geq_, rgb-eq_, hsl-eq_, for greyscale, RGB and HSL equalization resp.), and any previously generated convertions from those images will be overwritten. 


