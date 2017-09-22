#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 4: Delineate watershed based on TauDEM functions with PyGeoC

from pygeoc.TauDEM import TauDEMWorkflow, TauDEMFilesUtils, TauDEM


def main():
    """The simplest usage of watershed delineation based on TauDEM."""
    dem = '../tests/data/Jamaica_dem.tif'
    num_proc = 2

    TauDEMWorkflow.watershed_delineation(num_proc, dem)


if __name__ == "__main__":
    main()
