#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 3: Delineate watershed based on TauDEM functions with PyGeoC

from pygeoc.TauDEM import TauDEMFilesUtils, TauDEMWorkflow


def main():
    """Watershed delineation based on TauDEM."""
    dem = '../tests/data/Jamaica_dem.tif'
    outlet = None
    acc_thresh = 0
    distdown = 'v'
    wp = '../tests/data/tmp_results'
    td_names = TauDEMFilesUtils(wp)
    log_name = 'delineation_watershed.log'

    taudem_bin = None
    mpi_bin = None
    num_proc = 2

    TauDEMWorkflow.watershed_delineation(taudem_bin, mpi_bin, num_proc, dem, outlet, acc_thresh,
                                         distdown, td_names, log_name)


if __name__ == "__main__":
    main()
