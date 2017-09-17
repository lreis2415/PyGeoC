#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 2: Run TauDEM functions with PyGeoC
import os

from pygeoc.TauDEM import TauDEM
from pygeoc.raster import RasterUtilClass


def main():
    """run function of TauDEM."""
    dem = '../tests/data/Jamaica_dem.tif'
    wp = '../tests/data/tmp_results'
    fel = 'dem_pitremoved.tif'
    taudem_bin = None
    mpi_bin = None
    num_proc = 2

    TauDEM.fill(num_proc, wp, dem, fel, mpiexedir=mpi_bin, exedir=taudem_bin)

    rawdem = RasterUtilClass.read_raster(dem)
    feldem = RasterUtilClass.read_raster(wp + os.sep + fel)

    print ('RawDEM: Max: %.2f, Min: %.2f, Mean: %.2f' % (rawdem.get_max(), rawdem.get_min(),
                                                         rawdem.get_average()))
    print ('FilledDEM: Max: %.2f, Min: %.2f, Mean: %.2f' % (feldem.get_max(), feldem.get_min(),
                                                            feldem.get_average()))


if __name__ == "__main__":
    main()
