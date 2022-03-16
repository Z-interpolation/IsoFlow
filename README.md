# IsoFlow (Isotropic image interpolation using optical Flow)
Inputs a set of `N` images (all with the same resolution and depth) and outputs a set of `(f-1)(N-1)` images, where `f` (an integer power of 2 larger than 1) is the interpolation factor, generated using linear interpolation driven by the optical flow, as decribed in [*Optical Flow Driven Interpolation for Isotropic FIB-SEM Reconstructions*]().

Example:

    > ls *.tif
    img000.tif
    img001.tif
    img002.tif
    img003.tif
    > python interpolate.py -i img%3d.tif -f 2 -N 4
    > ls *.tif
    img000.tif  <- original image img000.tif
    img001.tif  <- interpolated image between original images img000.tif and img001.tif
    img002.tif  <- original image img001.tif
    img003.tif  <- interpolated image between original images img001.tif and img002.tif
    img004.tif  <- original image img002.tif 
    img005.tif  <- interpolated image between original images img002.tif and img003.tif
    img006.tif  <- original image img003.tif
    
In this [manual]() you will find more cases of use and extra details about this tool.
