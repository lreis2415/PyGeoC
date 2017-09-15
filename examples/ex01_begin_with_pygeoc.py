#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Welcome to PyGeoC (Python for GeoComputation) Tutorial.

# Exercise 1: Begin with PyGeoC
# Author: Liang-Jun Zhu
# Date: 9/9/2017
#
import os

try:
    from pygeoc.raster.raster import RasterUtilClass
except ImportError:
    print ("ERROR: PyGeoC is not successfully installed or contained within your project,"
           " please check and retry!")
    exit(-1)


def main():
    """Read GeoTiff raster data and print statistics.

    Returns:
        None
    """
    input_tif = "..%sdata%sJamaica_dem.tif" % (os.sep, os.sep)
    rst = RasterUtilClass.read_raster(input_tif)
    # metadata information
    print ("rows: %d, cols: %d" % (rst.nRows, rst.nCols))
    print ("LLCornerX: %f, LLCornerY: %f" % (rst.xMin, rst.yMin))
    print ("cell size: %f" % rst.dx)
    print ("Coornate system (if stated): %s" % rst.srs)
    # basic statistics, nodata is excluded
    print ("mean: %f, max: %f, min: %f" % (rst.get_average(), rst.get_max(), rst.get_min()))
    print ("std: %f, sum: %f" % (rst.get_std(), rst.get_sum()))


if __name__ == "__main__":
    main()
