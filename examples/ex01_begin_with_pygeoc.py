#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 1: Begin with PyGeoC

from pygeoc.raster import RasterUtilClass


def main():
    """Read GeoTiff raster data and print statistics.
    The output will be::

        rows: 130, cols: 100
        LLCornerX: 755145.28, LLCornerY: 654294.06
        cell size: 10.0
        mean: 203.92, max: 284.07, min: 139.11
        std: 32.32, sum: 2650967.00

    """
    input_tif = "../tests/data/Jamaica_dem.tif"
    rst = RasterUtilClass.read_raster(input_tif)
    # metadata information
    print ("rows: %d, cols: %d" % (rst.nRows, rst.nCols))
    print ("LLCornerX: %.2f, LLCornerY: %.2f" % (rst.xMin, rst.yMin))
    print ("cell size: %.1f" % rst.dx)
    # basic statistics, nodata is excluded
    print ("mean: %.2f, max: %.2f, min: %.2f" % (rst.get_average(), rst.get_max(), rst.get_min()))
    print ("std: %.2f, sum: %.2f" % (rst.get_std(), rst.get_sum()))


if __name__ == "__main__":
    main()
