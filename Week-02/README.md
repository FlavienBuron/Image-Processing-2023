## Assignment 2 (Week 2)

This code generates a Universal Color Table of 216 colors that is common to all images (independently of them), and an Adaptive Color Table of 216 colors for each provided images according to their color values distribution.

To run the code execute the following command:
```bash
python indexed_colors.py 
```

This will output the following:
* an image of the Universal Color Table, created by generating 6 linearly spaced values between 0 and 255 for each color channels.
* an image of the Adaptive Table for each input, created by generating 6 linearly spaced values between (mean - 2*std) and (mean + 2*std) for each color channels. Assuming a normal distribution for the values in each channels this would cover ~95% of the existing value, and a better representation of the true colors of an image (unless the values are very spread out over the possible range)

All images present in the folder `/in/` will be used and outputs are placed in the folder `/out/` with a prefix according to the color table (universal_, adaptive_), and any previously generated convertions from those images will be overwritten. 


