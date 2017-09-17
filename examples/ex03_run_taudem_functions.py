#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 3: Run TauDEM functions with PyGeoC
import os

from pygeoc.TauDEM import TauDEM
from pygeoc.raster import RasterUtilClass


def pitremove_example():
    """run function of TauDEM, take pitremove as an example.
    Compare the max, min, and average of rawdem and filled DEM.
    The result will be::

        RawDEM: Max: 284.07, Min: 139.11, Mean: 203.92
        FilledDEM: Max: 284.07, Min: 139.11, Mean: 203.93

    """
    dem = '../tests/data/Jamaica_dem.tif'
    wp = '../tests/data/tmp_results'
    fel = 'dem_pitremoved.tif'
    taudem_bin = None
    mpi_bin = None
    num_proc = 2

    TauDEM.pitremove(num_proc, dem, fel, wp, mpiexedir=mpi_bin, exedir=taudem_bin)

    rawdem = RasterUtilClass.read_raster(dem)
    feldem = RasterUtilClass.read_raster(wp + os.sep + fel)

    print ('RawDEM: Max: %.2f, Min: %.2f, Mean: %.2f' % (rawdem.get_max(), rawdem.get_min(),
                                                         rawdem.get_average()))
    print ('FilledDEM: Max: %.2f, Min: %.2f, Mean: %.2f' % (feldem.get_max(), feldem.get_min(),
                                                            feldem.get_average()))


if __name__ == "__main__":
    pitremove_example()
