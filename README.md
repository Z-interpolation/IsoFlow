# IsoFlow (Isotropic image interpolation using optical Flow)
Inputs a set of `N` images (all with the same resolution and depth) and outputs a set of `(f-1)(N-1)` images, where `f` (an integer power of 2 larger than 1) is the interpolation factor, generated using linear interpolation driven by the optical flow, as decribed in [*Optical Flow Driven Interpolation for Isotropic FIB-SEM Reconstructions*]().

Example:

    > ls *.tif
    img_000.tif
    img_001.tif
    img_002.tif
    img_003.tif
    > python linear_OF.py --images img_%3d.tif --interpolation_factor 2 --number_of_images 4
    > ls *.tif
    img_000.tif  <- original image img_000.tif
    img_001.tif  <- interpolated image between images img_000.tif and img_002.tif
    img_002.tif  <- original image img_001.tif
    img_003.tif  <- interpolated image between images img_002.tif and img_004.tif
    img_004.tif  <- original image img_002.tif 
    img_005.tif  <- interpolated image between images img_004.tif and img_006.tif
    img_006.tif  <- original image img_003.tif

In this [manual]() you will find more cases of use and extra details about this tool.
