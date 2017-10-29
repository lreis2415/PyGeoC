#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 7: Handling raster data with numpy, e.g., log transformation.

import numpy as np

from pygeoc.raster import RasterUtilClass


def main():
    """Read GeoTiff raster data and perform log transformation.
    """
    input_tif = "../tests/data/Jamaica_dem.tif"
    output_tif = "../tests/data/tmp_results/log_dem.tif"
    rst = RasterUtilClass.read_raster(input_tif)
    # raster data (with noDataValue as numpy.nan) as numpy array
    rst_valid = rst.validValues
    output_data = np.log(rst_valid)
    # write output raster
    RasterUtilClass.write_gtiff_file(output_tif, rst.nRows, rst.nCols, output_data, rst.geotrans,
                                     rst.srs, rst.noDataValue, rst.dataType)


if __name__ == "__main__":
    main()
