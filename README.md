# MRC_interpolator
Inputs a MRC file, an interpolation factor '-f' (2, 4, ...) and an axis '-a' (X, Y or Z), and outputs an interpolated MRC file using the algorithm described in [*Optical Flow Driven Interpolation for Isotropic FIB-SEM Reconstructions*]().

Example:

    python interpolate.py -i input.mrc -o output.mrc -a Z -f 2
