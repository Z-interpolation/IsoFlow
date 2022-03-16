# IsoFlow (Isotropic image interpolator using optical Flow)
Inputs a set of `N` TIFF images (all with the same resolution and depth) and an interpolation factor (`f=2`,`4`, ...), and outputs a set of `(f-1)(N-1)+N` (from which `(f-1)(N-1)+N` are interpolated) TIFF images using linear interpolation driven by optical flow, as decribed in [*Optical Flow Driven Interpolation for Isotropic FIB-SEM Reconstructions*]().

Example:

    python interpolate.py -i input_prefix -o output.mrc -a Z -f 2
