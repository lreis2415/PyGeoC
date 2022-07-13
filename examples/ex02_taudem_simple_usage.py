# -*- coding: utf-8 -*-
# Exercise 2: Run TauDEM functions with PyGeoC
import os, sys

from pygeoc.TauDEM import TauDEM
from pygeoc.utils import UtilClass


def pitremove_simple_usage():
    """Simple usage of pitremove.
    Workspace will be set as the base directory of input file.
    """
    cur_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    dem = cur_dir + '/../tests/data/Jamaica_dem.tif'
    wp = cur_dir + '/../tests/data/tmp_results'
    UtilClass.mkdir(wp)
    fel = wp + '/dem_pitremoved.tif'
    num_proc = 2

    TauDEM.pitremove(num_proc, dem, fel)


if __name__ == "__main__":
    pitremove_simple_usage()
