# -*- coding: utf-8 -*-
# Exercise 3: Run TauDEM functions with PyGeoC
import os,sys

from pygeoc.TauDEM import TauDEM
from pygeoc.raster import RasterUtilClass
from pygeoc.utils import UtilClass


def pitremove_example():
    """run function of TauDEM, take pitremove as an example.
    Compare the max, min, and average of rawdem and filled DEM.
    The result will be::

        RawDEM: Max: 284.07, Min: 139.11, Mean: 203.92
        FilledDEM: Max: 284.07, Min: 139.11, Mean: 203.93

    """
    cur_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    dem = cur_dir + '/../tests/data/Jamaica_dem.tif'
    wp = cur_dir + '/../tests/data/tmp_results'
    fel = 'dem_pitremoved.tif'
    taudem_bin = None
    mpi_bin = None
    num_proc = 2

    UtilClass.mkdir(wp)
    TauDEM.pitremove(num_proc, dem, fel, wp, mpiexedir=mpi_bin, exedir=taudem_bin)

    rawdem = RasterUtilClass.read_raster(dem)
    feldem = RasterUtilClass.read_raster('%s/%s' % (wp, fel))

    print('RawDEM: Max: %.2f, Min: %.2f, Mean: %.2f' % (rawdem.get_max(), rawdem.get_min(),
                                                        rawdem.get_average()))
    print('FilledDEM: Max: %.2f, Min: %.2f, Mean: %.2f' % (feldem.get_max(), feldem.get_min(),
                                                           feldem.get_average()))


if __name__ == "__main__":
    pitremove_example()
