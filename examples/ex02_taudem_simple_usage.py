#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 2: Run TauDEM functions with PyGeoC

from pygeoc.TauDEM import TauDEM


def pitremove_simple_usage():
    """Simple usage of pitremove.
    Workspace will be set as the base directory of input file.
    """
    dem = '../tests/data/Jamaica_dem.tif'
    fel = '../tests/data/tmp_results/dem_pitremoved.tif'
    num_proc = 2

    TauDEM.pitremove(num_proc, dem, fel)


if __name__ == "__main__":
    pitremove_simple_usage()
