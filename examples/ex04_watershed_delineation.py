# -*- coding: utf-8 -*-
# Exercise 4: Delineate watershed based on TauDEM functions with PyGeoC
import os, sys

from pygeoc.TauDEM import TauDEMFilesUtils, TauDEMWorkflow
from pygeoc.hydro import Hillslopes
from pygeoc.utils import UtilClass


def main():
    """The simplest usage of watershed delineation based on TauDEM."""
    cur_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    dem = cur_dir + '/../tests/data/Jamaica_dem.tif'
    num_proc = 2
    wp = cur_dir + '/../tests/data/tmp_results/wtsd_delineation'
    UtilClass.mkdir(wp)

    TauDEMWorkflow.watershed_delineation(num_proc, dem, workingdir=wp)

    namecfg = TauDEMFilesUtils(wp)
    streamf = namecfg.stream_raster
    flowdirf = namecfg.d8flow
    hillslpf = '%s/hillslope.tif' % wp

    Hillslopes.downstream_method_whitebox(streamf, flowdirf, hillslpf)


if __name__ == "__main__":
    main()
