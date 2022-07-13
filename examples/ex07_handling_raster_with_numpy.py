# -*- coding: utf-8 -*-
# Exercise 7: Handling raster data with numpy, e.g., log transformation.
import os, sys

import numpy as np

from pygeoc.raster import RasterUtilClass
from pygeoc.utils import UtilClass


def main():
    """Read GeoTiff raster data and perform log transformation.
    """
    cur_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    input_tif = cur_dir + '/../tests/data/Jamaica_dem.tif'
    wp = cur_dir + '/../tests/data/tmp_results'
    UtilClass.mkdir(wp)
    output_tif = wp + '/log_dem.tif'
    rst = RasterUtilClass.read_raster(input_tif)
    # raster data (with noDataValue as numpy.nan) as numpy array
    rst_valid = rst.validValues
    output_data = np.log(rst_valid)
    # write output raster
    RasterUtilClass.write_gtiff_file(output_tif, rst.nRows, rst.nCols, output_data, rst.geotrans,
                                     rst.srs, rst.noDataValue, rst.dataType)


if __name__ == "__main__":
    main()
