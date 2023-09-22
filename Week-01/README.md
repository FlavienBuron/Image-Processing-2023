## Assignment 1 (Week 1)

This code flips the provided image(s) in multiple orientations: horizontal, vertical or both at the same time

To run the code execute the following command:
```bash
python image_flip.py
```

By default the code output all flip orientations. To choose a specific orientation an argument can be added with `--orient X` where `X` can take one of the following values:
`h`, `v`, `both`, `all`. These will output an horizontal flip (single image output), vertical flip (single image output), an image flipped on both axis, or output an image 
for each of the previous orientation.

For example:
```bash
python image_flip.py --orient both
```
This will output a single image flipped vertically and horizontally.

All images present in the folder `/in/` will be used and outputs are placed in the folder `/out/` with a prefix according to the flip (h_, v_, vh_ (for both)), and any previously generated flips from those images will be overwritten. 

