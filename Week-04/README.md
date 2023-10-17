## Assigment 4 (Week 4)

Three scripts are available and respectively cover bluring (mean filtering), edge detection (Laplacian of Gaussian and gradient filter) and statistical filters (min, max, min-max), taking grayscale images as input

To run the code respectively execute the following commands:
```bash
python blur.py 
```
```bash
python edge.py
```
```bash
python stats.py
```

This will output the following:
* For `blur` an image with the application of the mean filter with a 3x3 kernel and a 5x5 kernel
* For `edge` an image with a Laplacian of Gaussian filter calculated with a kernel of size 3x3 and sigma of 1, as well as an image with the application of a Sobel filter (3x3)
* For `stats` an image for each application of the following filters, with size 3x3 and 5x5: min filter, max filter and max-min filter.

All images present in the folder `/in/` will be used and outputs are placed in the folder `/out/` with a prefix according to the filter applied, and any previously generated convertions from those images will be overwritten. 


