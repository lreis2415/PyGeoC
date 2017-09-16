#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 1: Begin with PyGeoC

from pygeoc.raster import RasterUtilClass


def main():
    """Read GeoTiff raster data and print statistics.

    Returns:
        None
    """
    input_tif = "../tests/data/Jamaica_dem.tif"
    rst = RasterUtilClass.read_raster(input_tif)
    # metadata information
    print ("rows: %d, cols: %d" % (rst.nRows, rst.nCols))
    print ("LLCornerX: %f, LLCornerY: %f" % (rst.xMin, rst.yMin))
    print ("cell size: %f" % rst.dx)
    if rst.srs is not None:
        print ("Coornate system: %s" % rst.srs)
    # basic statistics, nodata is excluded
    print ("mean: %f, max: %f, min: %f" % (rst.get_average(), rst.get_max(), rst.get_min()))
    print ("std: %f, sum: %f" % (rst.get_std(), rst.get_sum()))


if __name__ == "__main__":
    main()
