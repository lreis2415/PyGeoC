# -*- coding: utf-8 -*-

# Example 08: Given value's raster connectivity analysis.
# Based Theory: The 8-neighborhood pixels shared the same given value have the
# connectivity. These pixels which have connectivity will be classed in a
# same ID.
# Related modules: pygeoc.raster
# Created by Yan-Wen Wang
# Date: 2017.11
#
import os
import sys

import numpy as np

# If there is numba package in your PC, you can use this module to accelerate
# the program.
# from numba import jit
from pygeoc.raster import RasterUtilClass, GDT_Float32

# To avoid the Recursion Number Limit error: maximum recursion depth
# exceeded in cmp
sys.setrecursionlimit(1000000)


def pixels_connectivity_compute(raster, i, j, idx):
    """Compute if the two given value's pixels have connectivity

    Compute if the two given value's pixels of raster have connectivity between
    the [i.j]pixel and its 8-neighborhood. If they have connectivity,
    then put its neighborhood to List idx and go in a recursion. If the  [i,
    j]pixel and its neighborhood don't have connectivity, do nothing.

    Args:
        raster: A rasterfile stored pixels initial values.
        i: The pixel's x coord.
        j: The pixel's y coord.
        idx: A List stored pixels which have the same ID(means same that
        these pixels have connectivity)
    """
    nrows, ncols = raster.shape
    value = raster[i][j]
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if 0 <= i + di < nrows and 0 <= j + dj < ncols:
                if raster[i + di][j + dj] == value and not (di == dj and di == 0):
                    if [i + di, j + dj] not in idx:
                        idx.append([i + di, j + dj])
                        pixels_connectivity_compute(raster, i + di, j + dj, idx)


# If there is numba package in your PC, you can use @jit to accelerate the
# program
# @jit
def remove_existID_pixels(givenvalue_pixels_positions, idx_array):
    """Delete the existed ID pixels who's in nparray idx_array

    After computing pixels connectivity, we get a set of pixels which have
    connectivity and have the same ID. We get these pixels positions set as
    nparray idx_array as well. Then we need to remove these pixels from all
    of the given value's pixels and compute the connectivity of rest given
    value's pixels.

    Args:
        givenvalue_pixels_positions: given value's pixels positions set from
        last time's computing connectivity.
        idx_array: pixels position set which have the same ID(means same that
        these pixels have connectivity)

    Return:
        givenvalue_pixels_positions: given value's pixels positions set
        after deleting the existed ID pixels.
    """
    # We need to give List existID_pixels a 0 value to avoid the error:
    # cannot compute fingerprint of empty list
    existID_pixels = [0]
    for i in range(givenvalue_pixels_positions.shape[0]):
        for j in range(idx_array.shape[0]):
            if ((givenvalue_pixels_positions[i, 0] == idx_array[j, 0]) and
                    (givenvalue_pixels_positions[i, 1] == idx_array[j, 1])):
                existID_pixels.append(i)
    givenvalue_pixels_positions = np.delete(givenvalue_pixels_positions,
                                            existID_pixels, 0)
    return givenvalue_pixels_positions


# If there is numba package in your PC, you can use @jit to accelerate the
# program
# @jit
def draw_ID(ID, idx_array, drawID_raster):
    """Draw every pixel's ID

    After computing all given value's pixels connectivity, every pixel will
    have an ID. Then we need to draw these pixels' ID on the undrawed
    rasterfile.

    Args:
        ID: given ID value
        idx_array: pixels position set which have the given ID value
        drawID_raster: undrawed rasterfile

    Return:
        drawID_raster: rasterfile after drawing ID
    """
    for i in range(idx_array.shape[0]):
        x = idx_array[i, 0]
        y = idx_array[i, 1]
        drawID_raster[x, y] = ID
    return drawID_raster


if __name__ == "__main__":
    # Example: Compute the craters pixels' connectivity and draw an ID rasterfile.
    cur_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    inputRaster = cur_dir + "/../tests/data/RFCalcTest1Craters-PostProcessing.tif"
    RasterData = RasterUtilClass.read_raster(inputRaster)
    # Get the initial set: givenvalue_pixels_positions
    CratersCells = np.where(RasterData.data == 1)
    CratersCells = np.array(CratersCells)
    CratersCells = CratersCells.T

    # Initiate the first ID
    ID = 1
    # Initiate the drawID_raster
    CratersIDData = np.zeros((RasterData.nRows, RasterData.nCols))

    # Compute every pixels' connectivity
    while CratersCells.size > 0:
        cell = CratersCells[0]
        idx = [[cell[0], cell[1]]]
        # Compute the pixel and its 8-neighborhoods' connectivity
        pixels_connectivity_compute(RasterData.data, cell[0], cell[1], idx)
        # Get the pixels position set which have the last step's ID value
        idxArray = np.array(idx)
        # Remove the existed last step's ID pixels
        CratersCells = remove_existID_pixels(CratersCells, idxArray)
        # Draw the last step's ID pixels' ID value
        CratersIDData = draw_ID(ID, idxArray, CratersIDData)
        # ID need to add 1 for next time's computing
        ID = ID + 1

    RasterUtilClass.write_gtiff_file(cur_dir + "/../tests/data/tmp_results/OldTest1CratersID.tif",
                                     RasterData.nRows, RasterData.nCols,
                                     CratersIDData, RasterData.geotrans,
                                     RasterData.srs, -9999, GDT_Float32)
