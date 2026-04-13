# -*- coding: utf-8 -*-
"""Utility Classes and Functions

    @author: Liangjun Zhu

    @changlog:

     - 12-04-12 jz - origin version.
     - 16-07-01 lj - reorganized for pygeoc.
     - 17-06-25 lj - check by pylint and reformat by Google style.
     - 18-10-31 lj - add type hints according to typing package.
"""
from __future__ import division, unicode_literals
from future.utils import iteritems

import argparse
from configparser import ConfigParser
import glob
import os
import platform
import re
import socket
import subprocess
import time
from datetime import datetime
from math import sqrt
from shutil import copy, rmtree
from typing import Optional, List, Union, Tuple, Dict, Any, AnyStr

try:
    import numpy
except ImportError:
    print('numpy is not installed, some functions cannot be used!')

sysstr = platform.system()

# Global constants
SQ2 = 1.4142135623730951
"""approximate of square root of 2."""
PI = 3.14159265358979323846
"""approximate value of pi."""
ZERO = 1e-12
"""approximate of zero."""
DELTA = 1e-6
"""Delta value to check two approximately equal floats."""
DEFAULT_NODATA = -9999.
"""Default NoData value for raster dataset."""


# Common used compatible functions on Python 2.7.x and Python 3.3+


def is_integer(v):
    # type: (...) -> bool
    """Test whether a value is an integer (of any kind).

    Examples:
        >>> is_integer(1)
        True
        >>> is_integer(-0.123)
        False
        >>> is_integer(3.)
        False
        >>> is_integer(9223372036854775808)
        True
        >>> is_integer('1')
        False
        >>> is_integer(None)
        False
        >>> is_integer(numpy.int32(3))
        True
    """
    try:
        from builtins import int
        return isinstance(v, (int, numpy.integer))  # Match both int and long on Py2
    except ImportError:
        from past.builtins import long
        return isinstance(v, (int, long, numpy.integer))


def is_string(in_str):
    # type: (...) -> bool
    """Test Unicode (text) string literal.

    Examples:
        >>> is_string('abc')
        True
        >>> is_string(u'abc')
        True
        >>> is_string(u'北京')
        True
        >>> is_string(123)
        False
        >>> is_string(None)
        False
        >>> is_string(['a', 'b'])
        False

        # Python 3
        # >>> is_string(b'avoid considering byte-strings as strings.')
        # False
    """
    return isinstance(in_str, (str, u''.__class__))


class MathClass(object):
    """Basic math related."""

    def __init__(self):
        pass

    @staticmethod
    def isnumerical(x):
        # type: (...) -> bool
        """Check the input x is numerical or not.

        Examples:
            >>> MathClass.isnumerical('78')
            True
            >>> MathClass.isnumerical('1.e-5')
            True
            >>> MathClass.isnumerical(None)
            False
            >>> MathClass.isnumerical('a1.2')
            False
            >>> MathClass.isnumerical(['1.2'])
            False
            >>> MathClass.isnumerical(numpy.float64(1.2))
            True

        """
        try:
            xx = float(x)
        except TypeError:
            return False
        except ValueError:
            return False
        except Exception:
            return False
        else:
            return True

    @staticmethod
    def floatequal(a, b):
        # type: (Union[int, float, numpy.ScalarType], Union[int, float, numpy.ScalarType]) -> bool
        """If float a is equal to float b.

        Examples:
            >>> MathClass.floatequal(1, 1.000001)  # 1 - 1.000001 likes -9.999999999177334e-07
            True
            >>> MathClass.floatequal(1, 1.0000001)
            True
            >>> MathClass.floatequal(2, 2.)
            True
            >>> MathClass.floatequal(1, 1.00001)
            False
        """
        return abs(a - b) < DELTA

    @staticmethod
    def _check_pair_arrays(obsvalues, simvalues):
        # type: (...) -> Tuple[numpy.ndarray, numpy.ndarray]
        """Convert paird inputs to float arrays and remove NaN/Inf pairs.

        Examples:
            >>> obs = [1.0, 2.0, numpy.nan, 4.0]
            >>> sim = [1.1, 1.9, 3.0, numpy.inf]
            >>> o, s = MathClass._check_pair_arrays(obs, sim)
            >>> o.tolist()
            [1.0, 2.0]
            >>> s.tolist()
            [1.1, 1.9]
        """
        if len(obsvalues) != len(simvalues):
            raise ValueError("The size of observed and simulated values must be the same!")

        if not isinstance(obsvalues, numpy.ndarray):
            obsvalues = numpy.array(obsvalues, dtype=float)
        else:
            obsvalues = obsvalues.astype(float)

        if not isinstance(simvalues, numpy.ndarray):
            simvalues = numpy.array(simvalues, dtype=float)
        else:
            simvalues = simvalues.astype(float)

        valid = numpy.isfinite(obsvalues) & numpy.isfinite(simvalues)
        obsvalues = obsvalues[valid]
        simvalues = simvalues[valid]

        if len(obsvalues) == 0:
            raise ValueError(
                "No valid paired observed and simulated values remain after removing NaN/Inf!")

        return obsvalues, simvalues

    @staticmethod
    def _std(values,  # type: Union[numpy.ndarray, List[Union[float, int]]]
             ddof=0   # type: int
            ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate standard deviation with user-defined ddof.

        Examples:
            >>> vals = [1., 2., 3., 4.]
            >>> MathClass._std(vals)  # doctest: +ELLIPSIS
            1.118033988749895...
            >>> MathClass._std(vals, ddof=1)  # doctest: +ELLIPSIS
            1.2909944487358056...
            >>> vals = [1., 2., 3., 4., numpy.nan, numpy.inf]
            >>> MathClass._std(vals)  # doctest: +ELLIPSIS
            1.118033988749895...
            >>> MathClass._std(vals, ddof=1)  # doctest: +ELLIPSIS
            1.2909944487358056...
        """
        if not isinstance(values, numpy.ndarray):
            values = numpy.array(values, dtype=float)
        else:
            values = values.astype(float)

        values = values[numpy.isfinite(values)]
        if len(values) == 0:
            raise ValueError("No valid values for standard deviation calculation!")

        if ddof < 0:
            raise ValueError("ddof must be greater than or equal to 0!")
        if len(values) <= ddof:
            raise ValueError("The number of valid values must be greater than ddof!")

        return numpy.std(values, ddof=ddof)

    @staticmethod
    def nashcoef(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                 simvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                 log=False,  # type: bool
                 expon=2  # type: Union[float, int, numpy.ScalarType]
                 ):
        # type: (...) -> float
        """Calculate Nash-Sutcliffe coefficient(NSE) proposed by Nash and Sutcliffe (1970)
        and its variants.

           The following description is referred by Krause et al. (2005) and Moriasi et al. (2007).

             - The range of NSE lies between -inf and 1.0 (prefect fit).
             - Since the differences between observed and simulated values
               are calculated as squared values (expon=2), the larger values
               in a time series are strongly overestimated whereas lower
               values are neglected (Legates and McCabe, 1999). For the
               quantification of runoff prediction, this leads to an overestimation
               of the model performance during peak flows and an underestimation
               during low flow conditions.
             - Similar to R-square, NSE is not very sensitive to systematic
               model over- or underestimation especially during low flow periods.
             - To reduce the sensitivity of the original NSE to extreme values,
               the NSE is often calculated with logarithmic values of obseravtion
               and simulation values, which known as lnE. As a result, the
               influence of the low flow values is increased in comparison to the
               flood peaks resulting in an increase in sensitivity of lnE to
               systematic model over- or underestimation.
             - A more general form could be used for the same purpose as lnE, i.e.,
               varying the exponent from 1 to N. With the increase of `expon`, the
               sensitivity to high flows will increase and could be used when only
               the high flows are of interest, e.g., for flood prediction.

        Args:
            obsvalues: observation values array
            simvalues: simulation values array
            log: Do logarithmic transformation or not, False by default
            expon: The exponent range from 1 to N, 2 by default

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.nashcoef(obs, sim)  # doctest: +ELLIPSIS
            0.451803966838596...
            >>> MathClass.nashcoef(obs, sim, log=True)  # doctest: +ELLIPSIS
            0.2841143016830745...
            >>> MathClass.nashcoef(obs, sim, expon=1)  # doctest: +ELLIPSIS
            0.3959646306103376...
            >>> MathClass.nashcoef(obs, sim, expon=3)  # doctest: +ELLIPSIS
            0.6122272075952075...
            >>> MathClass.nashcoef(obs, sim, expon=14)  # doctest: +ELLIPSIS
            0...
            >>> MathClass.nashcoef(obs, sim, expon=0)  # doctest: +ELLIPSIS
            0...

        Returns:
            NSE, or raise exception
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)

        if log:  # Be care of zero values
            valid = (obsvalues > 0.) & (simvalues > 0.)
            obsvalues = obsvalues[valid]
            simvalues = simvalues[valid]
            if len(obsvalues) == 0:
                raise ValueError("No positive paired values available for log-NSE calculation!")
            obsvalues = numpy.log(obsvalues)
            simvalues = numpy.log(simvalues)
        if expon > len(obsvalues) or expon < 1:
            return 0.
        ave = numpy.nanmean(obsvalues)
        a1 = numpy.nansum(numpy.abs(obsvalues - simvalues) ** expon)
        a2 = numpy.nansum(numpy.abs(obsvalues - ave) ** expon)

        if MathClass.floatequal(a2, 0.):
            if numpy.allclose(obsvalues, simvalues):
                return 1.
            return 0.

        return 1. - a1 / a2

    @staticmethod
    def pearsonr(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                 simvalues  # type: Union[numpy.ndarray, List[Union[float, int]]]
                 ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate Pearson correlation coefficient (r).

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.pearsonr(obs, sim)  # doctest: +ELLIPSIS
            0.867689555679048...
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)

        if len(obsvalues) < 2:
            raise ValueError("At least two paired values are required for Pearson-r calculation!")

        obs_avg = numpy.mean(obsvalues)
        sim_avg = numpy.mean(simvalues)
        obs_minus_avg_sq = numpy.sum((obsvalues - obs_avg) ** 2)
        sim_minus_avg_sq = numpy.sum((simvalues - sim_avg) ** 2)
        obs_sim_minus_avgs = numpy.sum((obsvalues - obs_avg) * (simvalues - sim_avg))

        yy = obs_minus_avg_sq ** 0.5 * sim_minus_avg_sq ** 0.5
        if MathClass.floatequal(yy, 0.):
            if numpy.allclose(obsvalues, simvalues):
                return 1.
            return 0.

        return obs_sim_minus_avgs / yy

    @staticmethod
    def rsquare(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                simvalues  # type: Union[numpy.ndarray, List[Union[float, int]]]
                ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate Coefficient of determination.

        Same as the square of the Pearson correlation coefficient (r),
        and, the same as the built-in Excel function RSQ().
        Programmed according to equation (1) in
        
        Legates, D.R. and G.J. McCabe, 1999.  Evaluating the use of "goodness of fit" measures
        in hydrologic and hydroclimatic model variation.  Water Resources Research 35:233-241.

        Args:
            obsvalues: observe values array
            simvalues: simulate values array

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.rsquare(obs, sim)  # doctest: +ELLIPSIS
            0.7528851650345053...

        Returns:
            R-square value, or raise exception
        """
        cc = MathClass.pearsonr(obsvalues, simvalues)
        return cc ** 2.

    @staticmethod
    def mse(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
            simvalues  # type: Union[numpy.ndarray, List[Union[float, int]]]
            ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate MSE.

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.mse(obs, sim)  # doctest: +ELLIPSIS
            31.25846153846154...
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)
        return numpy.mean((obsvalues - simvalues) ** 2.)

    @staticmethod
    def rmse(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
             simvalues  # type: Union[numpy.ndarray, List[Union[float, int]]]
             ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate RMSE.

        Args:
            obsvalues: observe values array
            simvalues: simulate values array

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.rmse(obs, sim)  # doctest: +ELLIPSIS
            5.590926715533082...

        Returns:
            RMSE value
        """
        return numpy.sqrt(MathClass.mse(obsvalues, simvalues))

    @staticmethod
    def mae(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
            simvalues  # type: Union[numpy.ndarray, List[Union[float, int]]]
            ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate MAE.

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.mae(obs, sim)  # doctest: +ELLIPSIS
            2.983076923076923...
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)
        return numpy.mean(numpy.abs(obsvalues - simvalues))

    @staticmethod
    def pbias(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
              simvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
              sim_minus_obs = True  # type: bool
              ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate PBIAS (percent model bias).

        Note:
            Default sign convention is pySWATPlus-compatible:
                PBIAS = 100 * sum(sim - obs) / sum(obs)

            If you want to preserve the old convention, set sim_minus_obs=False:
                PBIAS = 100 * sum(obs - sim) / sum(obs)

        Args:
            obsvalues: observe values array
            simvalues: simulate values array

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.pbias(obs, sim)  # doctest: +ELLIPSIS
            -35.46099290780142...
            >>> MathClass.pbias(obs, sim, sim_minus_obs=False)  # doctest: +ELLIPSIS
            35.46099290780142...

        Returns:
            PBIAS value (percentage), or raise exception
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)
        obs_sum = numpy.sum(obsvalues)

        if MathClass.floatequal(obs_sum, 0.):
            raise ValueError("The sum of observed values is zero for PBIAS calculation!")

        if sim_minus_obs:
            return 100. * numpy.sum(simvalues - obsvalues) / obs_sum
        return 100. * numpy.sum(obsvalues - simvalues) / obs_sum

    @staticmethod
    def mare(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
             simvalues  # type: Union[numpy.ndarray, List[Union[float, int]]]
             ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate MARE (Mean Absolute Relative Error).

        Notes:
            Pairs with observed value == 0 are excluded to avoid division by zero.

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.mare(obs, sim)  # doctest: +ELLIPSIS
            0.5746910422728188...
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)
        valid = numpy.logical_not(numpy.isclose(obsvalues, 0.))
        obsvalues = obsvalues[valid]
        simvalues = simvalues[valid]

        if len(obsvalues) == 0:
            raise ValueError("No non-zero observed values available for MARE calculation!")

        return numpy.mean(numpy.abs((obsvalues - simvalues) / obsvalues))

    @staticmethod
    def rsr(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
            simvalues  # type: Union[numpy.ndarray, List[Union[float, int]]]
            ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate RSR (RMSE-to-SD Ratio).

        Programmed according to equation (3) in
        Moriasi et al. 2007.  Model evalutaion guidelines for systematic quantification of accuracy 
        in watershed simulations. Transactions of the ASABE 50(3): 885-900.

        Args:
            obsvalues: observe values array
            simvalues: simulate values array

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.rsr(obs, sim)  # doctest: +ELLIPSIS
            0.7404026155824978...

        Returns:
            RSR value, or raise exception
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)

        mean_obs = numpy.mean(obsvalues)
        numerator = numpy.sqrt(numpy.sum((obsvalues - simvalues) ** 2.))
        denominator = numpy.sqrt(numpy.sum((obsvalues - mean_obs) ** 2.))

        if MathClass.floatequal(denominator, 0.):
            if MathClass.floatequal(numerator, 0.):
                return 0.
            return numpy.inf

        return numerator / denominator

    @staticmethod
    def kge(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
            simvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
            ddof=0  # type: int
            ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate KGE (Kling-Gupta Efficiency).

        Notes:
            r = Pearson correlation coefficient
            alpha = std(sim) / std(obs)
            beta = mean(sim) / mean(obs)

        Args:
            obsvalues: observe values array
            simvalues: simulate values array
            ddof: Delta degrees of freedom used in standard deviation, 0 by default

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.kge(obs, sim)  # doctest: +ELLIPSIS
            0.27501928706851364...
            >>> MathClass.kge(obs, sim, ddof=1)  # doctest: +ELLIPSIS
            0.27501928706851364...
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)

        if len(obsvalues) < 2:
            raise ValueError("At least two paired values are required for KGE calculation!")

        obs_avg = numpy.mean(obsvalues)
        sim_avg = numpy.mean(simvalues)
        obs_std = MathClass._std(obsvalues, ddof=ddof)
        sim_std = MathClass._std(simvalues, ddof=ddof)

        if MathClass.floatequal(obs_avg, 0.):
            raise ValueError("The mean of observed values is zero for KGE calculation!")
        if MathClass.floatequal(obs_std, 0.):
            if numpy.allclose(obsvalues, simvalues):
                return 1.
            return 0.

        cc = MathClass.pearsonr(obsvalues, simvalues)
        alpha = sim_std / obs_std
        beta = sim_avg / obs_avg
        return 1. - numpy.sqrt((cc - 1.) ** 2 + (alpha - 1.) ** 2 + (beta - 1.) ** 2)

    @staticmethod
    def mkge(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
             simvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
             ddof=0  # type: int
             ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Calculate modified KGE (MKGE).

        Notes:
            gamma = (std(sim) / mean(sim)) / (std(obs) / mean(obs))

        Args:
            obsvalues: observe values array
            simvalues: simulate values array
            ddof: Delta degrees of freedom used in standard deviation, 0 by default

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.mkge(obs, sim)  # doctest: +ELLIPSIS
            0.44301113475711...
            >>> MathClass.mkge(obs, sim, ddof=1)  # doctest: +ELLIPSIS
            0.44301113475711...
        """
        obsvalues, simvalues = MathClass._check_pair_arrays(obsvalues, simvalues)

        if len(obsvalues) < 2:
            raise ValueError("At least two paired values are required for MKGE calculation!")

        obs_avg = numpy.mean(obsvalues)
        sim_avg = numpy.mean(simvalues)
        obs_std = MathClass._std(obsvalues, ddof=ddof)
        sim_std = MathClass._std(simvalues, ddof=ddof)

        if MathClass.floatequal(obs_avg, 0.) or MathClass.floatequal(sim_avg, 0.):
            raise ValueError("Mean observed or simulated values is zero for MKGE calculation!")
        if MathClass.floatequal(obs_std, 0.):
            if numpy.allclose(obsvalues, simvalues):
                return 1.
            return 0.

        cc = MathClass.pearsonr(obsvalues, simvalues)
        beta = sim_avg / obs_avg
        gamma = (sim_std / sim_avg) / (obs_std / obs_avg)
        return 1. - numpy.sqrt((cc - 1.) ** 2 + (beta - 1.) ** 2 + (gamma - 1.) ** 2)

    @staticmethod
    def performance_dict(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                         simvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                         ddof=0  # type: int
                         ):
        # type: (...) -> Dict[str, Union[float, numpy.ScalarType]]
        """Return a commonly used set of performance metrics.

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> sorted(MathClass.performance_dict(obs, sim).keys())
            ['KGE', 'MAE', 'MARE', 'MKGE', 'MSE', 'NSE', 'PBIAS', 'R', 'R2', 'RMSE', 'RSR', 'logNSE']
        """
        return {
            'NSE': MathClass.nashcoef(obsvalues, simvalues),
            'logNSE': MathClass.nashcoef(obsvalues, simvalues, log=True),
            'R': MathClass.pearsonr(obsvalues, simvalues),
            'R2': MathClass.rsquare(obsvalues, simvalues),
            'MSE': MathClass.mse(obsvalues, simvalues),
            'RMSE': MathClass.rmse(obsvalues, simvalues),
            'MAE': MathClass.mae(obsvalues, simvalues),
            'MARE': MathClass.mare(obsvalues, simvalues),
            'PBIAS': MathClass.pbias(obsvalues, simvalues),
            'RSR': MathClass.rsr(obsvalues, simvalues),
            'KGE': MathClass.kge(obsvalues, simvalues, ddof=ddof),
            'MKGE': MathClass.mkge(obsvalues, simvalues, ddof=ddof),
        }

    @staticmethod
    def indicator_names():
        # type: () -> Dict[str, str]
        """Return available performance indicator names.

        Examples:
            >>> sorted(MathClass.indicator_names().keys())
            ['KGE', 'MAE', 'MARE', 'MKGE', 'MSE', 'NSE', 'PBIAS', 'R', 'R2', 'RMSE', 'RSR', 'logNSE']
        """
        return {
            'NSE': 'Nash-Sutcliffe Efficiency',
            'logNSE': 'Log-transformed Nash-Sutcliffe Efficiency',
            'R': 'Pearson Correlation Coefficient',
            'R2': 'Coefficient of Determination',
            'MSE': 'Mean Squared Error',
            'RMSE': 'Root Mean Squared Error',
            'MAE': 'Mean Absolute Error',
            'MARE': 'Mean Absolute Relative Error',
            'PBIAS': 'Percent Bias',
            'RSR': 'RMSE-observations Standard deviation Ratio',
            'KGE': 'Kling-Gupta Efficiency',
            'MKGE': 'Modified Kling-Gupta Efficiency',
        }

    @staticmethod
    def _validate_indicator_abbr(indicator):
        # type: (str) -> None
        """Validate indicator abbreviation.

        Examples:
            >>> MathClass._validate_indicator_abbr('NSE')
            >>> MathClass._validate_indicator_abbr('ABC')
            Traceback (most recent call last):
            ...
            ValueError: Invalid indicator "ABC"; expected names are ['NSE', 'logNSE', 'R', 'R2', 'MSE', 'RMSE', 'MAE', 'MARE', 'PBIAS', 'RSR', 'KGE', 'MKGE']
        """
        abbr_indicator = MathClass.indicator_names()
        if indicator not in abbr_indicator:
            raise ValueError('Invalid indicator "%s"; expected names are %s'
                             % (indicator, list(abbr_indicator.keys())))

    @staticmethod
    def compute_from_abbr(obsvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                          simvalues,  # type: Union[numpy.ndarray, List[Union[float, int]]]
                          indicator,  # type: str
                          **kwargs  # type: Any
                          ):
        # type: (...) -> Union[float, numpy.ScalarType]
        """Compute performance metric from indicator abbreviation.

        Notes:
            Optional keyword arguments are passed to the target metric function.
            For example:
                - ddof for KGE and MKGE
                - sim_minus_obs for PBIAS
                - log / expon for NSE if indicator == 'NSE'

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.compute_from_abbr(obs, sim, 'NSE')  # doctest: +ELLIPSIS
            0.451803966838596...
            >>> MathClass.compute_from_abbr(obs, sim, 'R2')  # doctest: +ELLIPSIS
            0.7528851650345053...
            >>> MathClass.compute_from_abbr(obs, sim, 'KGE', ddof=0)  # doctest: +ELLIPSIS
            0.27501928706851364...
            >>> MathClass.compute_from_abbr(obs, sim, 'PBIAS')  # doctest: +ELLIPSIS
            -35.46099290780142...
            >>> MathClass.compute_from_abbr(obs, sim, 'PBIAS', sim_minus_obs=False)  # doctest: +ELLIPSIS
            35.46099290780142...
            >>> MathClass.compute_from_abbr(obs, sim, 'logNSE')  # doctest: +ELLIPSIS
            0.2841143016830745...
        """
        MathClass._validate_indicator_abbr(indicator)

        if indicator == 'NSE':
            return MathClass.nashcoef(obsvalues, simvalues, **kwargs)
        elif indicator == 'logNSE':
            # allow user override, but default log=True
            if 'log' not in kwargs:
                kwargs['log'] = True
            return MathClass.nashcoef(obsvalues, simvalues, **kwargs)
        elif indicator == 'R':
            return MathClass.pearsonr(obsvalues, simvalues)
        elif indicator == 'R2':
            return MathClass.rsquare(obsvalues, simvalues)
        elif indicator == 'MSE':
            return MathClass.mse(obsvalues, simvalues)
        elif indicator == 'RMSE':
            return MathClass.rmse(obsvalues, simvalues)
        elif indicator == 'MAE':
            return MathClass.mae(obsvalues, simvalues)
        elif indicator == 'MARE':
            return MathClass.mare(obsvalues, simvalues)
        elif indicator == 'PBIAS':
            return MathClass.pbias(obsvalues, simvalues, **kwargs)
        elif indicator == 'RSR':
            return MathClass.rsr(obsvalues, simvalues)
        elif indicator == 'KGE':
            return MathClass.kge(obsvalues, simvalues, **kwargs)
        elif indicator == 'MKGE':
            return MathClass.mkge(obsvalues, simvalues, **kwargs)

        raise ValueError('Unsupported indicator: %s' % indicator)

class StringClass(object):
    """String handling class
    """

    def __init__(self):
        """Empty"""
        pass

    @staticmethod
    def convert_str2num(unicode_str
                        # type: Union[AnyStr, int, float, List[Union[AnyStr, float, int]], Tuple[Union[AnyStr, float, int]]]
                        ):
        # type: (...) -> Union[AnyStr, int, float, List[Union[AnyStr, float, int]], Tuple[Union[AnyStr, float, int]]]
        """Convert string to string, integer, or float. Support tuple or list.

        Examples:
            >>> StringClass.convert_str2num('1.23')
            1.23
            >>> StringClass.convert_str2num(u'1.23')
            1.23
            >>> StringClass.convert_str2num(u'21.')
            21
            >>> StringClass.convert_str2num('abc123')
            'abc123'
            >>> StringClass.convert_str2num((123, u'2.3', 3., 'abc', u'edf'))
            (123, 2.3, 3, 'abc', 'edf')
            >>> StringClass.convert_str2num([123, u'2.3', 3., 'abc', u'edf'])
            [123, 2.3, 3, 'abc', 'edf']
        """
        if MathClass.isnumerical(unicode_str):
            unicode_str = float(unicode_str)
            if unicode_str % 1. == 0.:
                unicode_str = int(unicode_str)
            return unicode_str
        elif is_string(unicode_str):
            return str(unicode_str)
        elif isinstance(unicode_str, tuple):
            return tuple(StringClass.convert_str2num(v) for v in unicode_str)
        elif isinstance(unicode_str, list):
            return list(StringClass.convert_str2num(v) for v in unicode_str)
        else:
            return unicode_str

    @staticmethod
    def string_match(str1, str2):
        # type: (AnyStr, AnyStr) -> bool
        """Compare two string regardless capital or not"""
        return str1.lower() == str2.lower()

    @staticmethod
    def split_string(str_src, spliters=None, elim_empty=False):
        # type: (AnyStr, Union[AnyStr, List[AnyStr], None], bool) -> List[AnyStr]
        """Split string by split character space(' ') and indent('\t') as default

        Examples:
            >>> StringClass.split_string('exec -ini test.ini', ' ')
            ['exec', '-ini', 'test.ini']

        Args:
            str_src: source string
            spliters: e.g. [' ', '\t'], [], ' ', None
            elim_empty: Eliminate empty (i.e., '') or not.

        Returns:
            split sub-strings as list
        """
        if is_string(spliters):
            spliters = [spliters]
        if spliters is None or not spliters:
            spliters = [' ', '\t']
        dest_strs = list()
        src_strs = [str_src]
        while True:
            old_dest_strs = src_strs[:]
            for s in spliters:
                for src_s in src_strs:
                    temp_strs = src_s.split(s)
                    for temp_s in temp_strs:
                        temp_s = temp_s.strip()
                        if temp_s == '' and elim_empty:
                            continue
                        if is_string(temp_s):
                            temp_s = str(temp_s)
                        dest_strs.append(temp_s)
                src_strs = dest_strs[:]
                dest_strs = list()
            if old_dest_strs == src_strs:
                dest_strs = src_strs[:]
                break
        return dest_strs

    @staticmethod
    def is_substring(substr, str_src):
        # type: (AnyStr, AnyStr) -> bool
        """Is substr part of str_src, case insensitive."""
        return substr.lower() in str_src.lower()

    @staticmethod
    def string_in_list(tmp_str, strlist):
        # type: (AnyStr, List[AnyStr]) -> bool
        """Is tmp_str in strlist, case insensitive."""
        new_str_list = strlist[:]
        for i, str_in_list in enumerate(new_str_list):
            new_str_list[i] = str_in_list.lower()
        return tmp_str.lower() in new_str_list

    @staticmethod
    def is_valid_ip_addr(address):
        # type: (AnyStr) -> bool
        """Check the validation of IP address"""
        try:
            socket.inet_aton(address)
            return True
        except Exception:
            return False

    @staticmethod
    def extract_numeric_values_from_string(str_contains_values):
        # type: (AnyStr) -> Optional[List[Union[int, float]]]
        """
        Find numeric values from string, e.g., 1, .7, 1.2, 4e2, 3e-3, -9, etc.
        
        Reference: `how-to-extract-a-floating-number-from-a-string-in-python`_

        Examples:
            >>> input_str = '.1 .12 9.1 98.1 1. 12. 1 12'
            >>> StringClass.extract_numeric_values_from_string(input_str)
            [0.1, 0.12, 9.1, 98.1, 1, 12, 1, 12]
            >>> input_str = '-1 +1 2e9 +2E+09 -2e-9'
            >>> StringClass.extract_numeric_values_from_string(input_str)
            [-1, 1, 2000000000, 2000000000, -2e-09]
            >>> input_str = 'current level: -2.03e+2db'
            >>> StringClass.extract_numeric_values_from_string(input_str)
            [-203]

        Args:
            str_contains_values: string which may contains numeric values

        Returns:
            list of numeric values

        .. _how-to-extract-a-floating-number-from-a-string-in-python:
            https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string-in-python/4703508#4703508
        """
        numeric_const_pattern = r'[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?'
        rx = re.compile(numeric_const_pattern, re.VERBOSE)
        value_strs = rx.findall(str_contains_values)
        if len(value_strs) == 0:
            return None
        else:
            return [int(float(v)) if float(v) % 1. == 0 else float(v) for v in value_strs]

    @staticmethod
    def get_datetime(formatted_str, user_fmt=None):
        # type: (AnyStr, Optional[AnyStr]) -> datetime
        """get datetime() object from string formatted %Y-%m-%d %H:%M:%S

        Examples:
            >>> StringClass.get_datetime('2008-11-9')
            datetime.datetime(2008, 11, 9, 0, 0)
            >>> StringClass.get_datetime('2008/11/9')
            datetime.datetime(2008, 11, 9, 0, 0)
            >>> StringClass.get_datetime('20081109')
            datetime.datetime(2008, 11, 9, 0, 0)
            >>> StringClass.get_datetime('11/9/2008')
            datetime.datetime(2008, 11, 9, 0, 0)
            >>> StringClass.get_datetime('11-9-2008')
            datetime.datetime(2008, 11, 9, 0, 0)
            >>> StringClass.get_datetime('11/09/08')
            datetime.datetime(2008, 11, 9, 0, 0)
            >>> StringClass.get_datetime('2008-11-9 11:09')
            datetime.datetime(2008, 11, 9, 11, 9)
            >>> StringClass.get_datetime('2008-11-9 11:09:52')
            datetime.datetime(2008, 11, 9, 11, 9, 52)
        """
        date_fmts = ['%m-%d-%Y', '%Y-%m-%d', '%m-%d-%y', '%y-%m-%d']
        date_fmts += [d.replace('-', '/') for d in date_fmts]
        date_fmts += [d.replace('-', '') for d in date_fmts]
        time_fmts = ['%H:%M', '%H:%M:%S']
        fmts = date_fmts + ['%s %s' % (d, t) for d in date_fmts for t in time_fmts]
        if user_fmt is not None:
            if is_string(user_fmt):
                fmts.insert(0, str(user_fmt))
            elif isinstance(user_fmt, list):
                fmts = user_fmt + fmts
            elif isinstance(user_fmt, tuple):
                for fff in user_fmt:
                    fmts.insert(0, fff)
        flag = False
        for fmt in fmts:
            try:
                org_time = time.strptime(formatted_str, fmt)
                flag = True
                break
            except ValueError:
                pass
        if not flag:
            raise ValueError('The DATETIME must be one of the formats: %s' % ','.join(fmts))
        else:
            return datetime(org_time.tm_year, org_time.tm_mon, org_time.tm_mday,
                            org_time.tm_hour, org_time.tm_min, org_time.tm_sec)


class FileClass(object):
    """File IO related"""

    def __init__(self):
        """Empty"""
        pass

    @staticmethod
    def is_file_exists(filename):
        # type: (AnyStr) -> bool
        """Check the existence of file path."""
        if filename is None or not os.path.exists(filename) or not os.path.isfile(filename):
            return False
        else:
            return True

    @staticmethod
    def is_dir_exists(dirpath):
        # type: (AnyStr) -> bool
        """Check the existence of folder path."""
        if dirpath is None or not os.path.exists(dirpath) or not os.path.isdir(dirpath):
            return False
        else:
            return True

    @staticmethod
    def check_file_exists(filename):
        # type: (AnyStr) -> None
        """Throw exception if the file not existed"""
        if not FileClass.is_file_exists(filename):
            UtilClass.error("Input files path %s is None or not existed!\n" % filename)

    @staticmethod
    def copy_files(filename, dstfilename):
        # type: (AnyStr, AnyStr) -> None
        """Copy files with the same name and different suffixes, such as ESRI Shapefile."""
        FileClass.remove_files(dstfilename)
        dst_prefix = os.path.splitext(dstfilename)[0]
        pattern = os.path.splitext(filename)[0] + '.*'
        for f in glob.iglob(pattern):
            ext = os.path.splitext(f)[1]
            dst = dst_prefix + ext
            copy(f, dst)

    @staticmethod
    def remove_files(filename):
        # type: (AnyStr) -> None
        """
        Delete all files with same root as fileName,
        i.e. regardless of suffix, such as ESRI shapefile
        """
        pattern = os.path.splitext(filename)[0] + '.*'
        for f in glob.iglob(pattern):
            os.remove(f)

    @staticmethod
    def is_up_to_date(outfile, basedatetime):
        # type: (AnyStr, datetime) -> bool
        """Return true if outfile exists and is no older than base datetime."""
        if os.path.exists(outfile):
            if os.path.getmtime(outfile) >= basedatetime:
                return True
        return False

    @staticmethod
    def get_executable_fullpath(name, dirname=None, raise_exception=True):
        # type: (AnyStr, Optional[AnyStr], Optional[bool]) -> Optional[List[AnyStr]]
        """get the full path of a given executable name"""
        if name is None:
            return None
        if is_string(name):
            name = str(name)
        else:
            raise RuntimeError('The input function name or path must be string!')
        if dirname is not None:  # check the given path first
            dirname = os.path.abspath(dirname)
            fpth = dirname + os.sep + name
            if os.path.isfile(fpth):
                return fpth
        # If dirname is not specified, check the env then.
        if sysstr == 'Windows':
            findout = UtilClass.run_command('where %s' % name, raise_exception)
        else:
            findout = UtilClass.run_command('which %s' % name, raise_exception)
        if not findout or len(findout) == 0:
            if raise_exception:
                print("%s is not included in the env path" % name)
                exit(-1)
            else:
                return None
        first_path = findout[0].split('\n')[0]
        if os.path.exists(first_path):
            return FileClass.get_file_fullpath_string(first_path)

        return None

    @staticmethod
    def get_file_fullpath(name, dirname=None):
        # type: (AnyStr, Optional[AnyStr]) -> Optional[AnyStr]
        """Return full path if available."""
        if name is None:
            return None
        if is_string(name):
            name = str(name)
        else:
            raise RuntimeError('The input function name or path must be string!')
        for sep in ['\\', '/', os.sep]:  # Loop all possible separators
            if sep in name:  # name is full path already
                name = os.path.abspath(name)
                return name
        if dirname is not None:
            dirname = os.path.abspath(dirname)
            name = dirname + os.sep + name
        return name

    @staticmethod
    def get_file_fullpath_string(name, dirname=None):
        # type: (AnyStr, Optional[AnyStr]) -> Optional[AnyStr]
        """Return full path in string format, to avoid failure caused by spaces in file path"""
        fullpath = FileClass.get_file_fullpath(name, dirname=dirname)
        if fullpath is None:
            return None
        if ' ' in fullpath and fullpath[0] != '\"' and fullpath[-1] != '\"':
            return '\"%s\"' % fullpath  # in case of spaces in the path
        else:
            return fullpath

    @staticmethod
    def get_filename_by_suffixes(dir_src, suffixes):
        # type: (AnyStr, Union[AnyStr, List[AnyStr]]) -> Optional[List[AnyStr]]
        """get file names with the given suffixes in the given directory

        Args:
            dir_src: directory path
            suffixes: wanted suffixes list, the suffix in suffixes can with or without '.'

        Returns:
            file names with the given suffixes as list
        """
        list_files = os.listdir(dir_src)
        re_files = list()
        if is_string(suffixes):
            suffixes = [suffixes]
        if not isinstance(suffixes, list):
            return None
        for i, suf in enumerate(suffixes):
            if len(suf) >= 1 and suf[0] != '.':
                suffixes[i] = '.' + suf
        for f in list_files:
            name, ext = os.path.splitext(f)
            if StringClass.string_in_list(ext, suffixes):
                re_files.append(f)
        return re_files

    @staticmethod
    def get_full_filename_by_suffixes(dir_src, suffixes):
        # type: (AnyStr, Union[AnyStr, List[AnyStr]]) -> Optional[List[AnyStr]]
        """get full file names with the given suffixes in the given directory

        Args:
            dir_src: directory path
            suffixes: wanted suffixes

        Returns:
            full file names with the given suffixes as list
        """
        file_names = FileClass.get_filename_by_suffixes(dir_src, suffixes)
        if file_names is None:
            return None
        return list(dir_src + os.sep + name for name in file_names)

    @staticmethod
    def get_core_name_without_suffix(file_path):
        # type: (AnyStr) -> AnyStr
        """Return core file name without suffix.

        Examples:
            >>> FileClass.get_core_name_without_suffix(r'/home/zhulj/1990.01.30/test.01.tif')
            'test.01'
            >>> FileClass.get_core_name_without_suffix(r'C:\zhulj\igsnrr\lreis.txt')
            'lreis'
            >>> FileClass.get_core_name_without_suffix(r'C:\\zhulj\\igsnrr\\lreis.txt')
            'lreis'
            >>> FileClass.get_core_name_without_suffix(r'C:/zhulj/igsnrr/lreis.txt')
            'lreis'
            >>> FileClass.get_core_name_without_suffix(r'/home/zhulj/dta/taudem/aread8')
            'aread8'
            >>> FileClass.get_core_name_without_suffix('singlename')
            'singlename'
            >>> FileClass.get_core_name_without_suffix('singlename.txt')
            'singlename'
        """
        if '\\' in file_path:
            file_path = file_path.replace('\\', '/')
        file_name = os.path.basename(file_path)
        core_names = file_name.split('.')
        if len(core_names) > 1:
            core_names = core_names[:-1]
        if isinstance(core_names, list):
            return str('.'.join(core_names))
        else:
            return str(core_names)

    @staticmethod
    def add_postfix(file_path, postfix):
        # type: (AnyStr, AnyStr) -> AnyStr
        """Add postfix for a full file path.

        Examples:
            >>> FileClass.add_postfix('/home/zhulj/dem.tif', 'filled')
            '/home/zhulj/dem_filled.tif'
            >>> FileClass.add_postfix('dem.tif', 'filled')
            'dem_filled.tif'
            >>> FileClass.add_postfix('dem', 'filled')
            'dem_filled'
        """
        cur_sep = ''
        for sep in ['\\', '/', os.sep]:
            if sep in file_path:
                cur_sep = sep
                break
        corename = FileClass.get_core_name_without_suffix(file_path)
        tmpspliter = os.path.basename(file_path).split('.')
        suffix = ''
        if len(tmpspliter) > 1:
            suffix = tmpspliter[-1]
        newname = os.path.dirname(file_path) + cur_sep + corename + '_' + postfix
        if suffix != '':
            newname += '.' + suffix
        return str(newname)


class DateClass(object):
    """Utility function to handle datetime."""

    def __init__(self):
        """Empty"""
        pass

    @staticmethod
    def is_leapyear(year):
        # type: (int) -> bool
        """Is leap year?

        Examples:
            >>> DateClass.is_leapyear(2000)
            True
            >>> DateClass.is_leapyear(2010)
            False
            >>> DateClass.is_leapyear(2004)
            True
            >>> DateClass.is_leapyear(2018)
            False
        """
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @staticmethod
    def day_of_month(year, month):
        # type: (int, int) -> int
        """Day number of month"""
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif DateClass.is_leapyear(year):
            return 29
        else:
            return 28

    @staticmethod
    def day_of_year(dt):
        # type: (int) -> int
        """Day index of year from 1 to 365 or 366"""
        sec = time.mktime(dt.timetuple())
        t = time.localtime(sec)
        return t.tm_yday


class UtilClass(object):
    """Other common used utility functions"""

    def __init__(self):
        """Empty"""
        pass

    @staticmethod
    def run_command(commands, raise_exception=True, prior_envpath=None):
        # type: (Union[AnyStr, List[AnyStr]], Optional[bool], Optional[AnyStr, List[AnyStr], Dict[AnyStr, AnyStr]]) -> Optional[None, List[AnyStr]]
        """Execute external command, and return the output lines list. In windows, refers to
        `handling-subprocess-crash-in-windows`_.

        Args:
            commands: string or list
            raise_exception: raise exception or not
            prior_envpath: prior search paths, string, list, or dict

        Returns:
            output lines

        .. _handling-subprocess-crash-in-windows:
            https://stackoverflow.com/questions/5069224/handling-subprocess-crash-in-windows
        """
        # commands = StringClass.convert_unicode2str(commands)
        # print(commands)

        use_shell = False
        subprocess_flags = 0
        startupinfo = None
        if sysstr == 'Windows':
            if isinstance(commands, list):
                commands = ' '.join(str(c) for c in commands)
            import ctypes
            SEM_NOGPFAULTERRORBOX = 0x0002  # From MSDN
            ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)
            subprocess_flags = 0x8000000  # win32con.CREATE_NO_WINDOW?
            # this startupinfo structure prevents a console window from popping up on Windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # not sure if node outputs on stderr or stdout so capture both
        else:  # for Linux/Unix OS, commands is better to be a list.
            if is_string(commands):
                use_shell = True
                # https://docs.python.org/2/library/subprocess.html
                #     Using shell=True can be a security hazard.
            elif isinstance(commands, list):
                # the executable path may be enclosed with quotes, if not windows, delete the quotes
                if commands[0][0] == commands[0][-1] == '"' or \
                        commands[0][0] == commands[0][-1] == "'":
                    commands[0] = commands[0][1:-1]
                for idx, v in enumerate(commands):
                    if isinstance(v, int) or isinstance(v, float):
                        # Fix :TypeError: execv() arg 2 must contain only strings
                        commands[idx] = repr(v)
        print(commands)

        # insert prior search paths for executables if specified, otherwise use the default PATH
        envpaths = os.environ.copy()
        if prior_envpath is not None:
            if type(prior_envpath) is dict:
                envpaths.update(prior_envpath)
            elif type(prior_envpath) is list:
                for ipath in reversed(prior_envpath):
                    envpaths['PATH'] = ipath + os.pathsep + envpaths['PATH']
            elif type(prior_envpath) is str:
                envpaths['PATH'] = prior_envpath + os.pathsep + envpaths['PATH']
            else:
                print('prior_envpath for run_command should be string, list, or dict!')

        process = subprocess.Popen(commands, shell=use_shell, stdout=subprocess.PIPE,
                                   stdin=open(os.devnull),
                                   stderr=subprocess.STDOUT, universal_newlines=True,
                                   startupinfo=startupinfo, env=envpaths,
                                   creationflags=subprocess_flags)
        try:
            out, err = process.communicate()
            recode = process.returncode
        except UnicodeDecodeError as unidecodeerr:
            print(unidecodeerr)
            return []

        if out is None:
            return ['']
        if recode is not None and recode != 0:
            if raise_exception:
                raise subprocess.CalledProcessError(-1, commands,
                                                    "ERROR occurred when running subprocess!")
            else:
                return None
        if '\n' in out:
            return out.split('\n')

        return [out]

    @staticmethod
    def current_path(local_function):
        """Get current path, refers to `how-do-i-get-the-path-of-the-current-executed-file-in-python`_

        Examples:

            .. code-block:: Python

               from pygeoc.utils import UtilClass
               curpath = UtilClass.current_path(lambda: 0)

        .. _how-do-i-get-the-path-of-the-current-executed-file-in-python:
            https://stackoverflow.com/questions/2632199/how-do-i-get-the-path-of-the-current-executed-file-in-python/18489147#18489147
        """
        from inspect import getsourcefile
        fpath = getsourcefile(local_function)
        if fpath is None:
            return None
        return os.path.dirname(os.path.abspath(fpath))

    @staticmethod
    def mkdir(dir_path):
        # type: (AnyStr) -> None
        """Make directory if not existed"""
        if not os.path.isdir(dir_path) or not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def rmmkdir(dir_path):
        # type: (AnyStr) -> None
        """If directory existed, then remove and make; else make it."""
        if not os.path.isdir(dir_path) or not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            rmtree(dir_path, True)
            os.makedirs(dir_path)

    @staticmethod
    def print_msg(contentlist):
        # type: (Union[AnyStr, List[AnyStr], Tuple[AnyStr]]) -> AnyStr
        """concatenate message list as single string with line feed."""
        if isinstance(contentlist, list) or isinstance(contentlist, tuple):
            return '\n'.join(contentlist)
        else:  # strings
            if len(contentlist) > 1 and contentlist[-1] != '\n':
                contentlist += '\n'
            return contentlist

    @staticmethod
    def error(msg):
        """throw RuntimeError exception"""
        raise RuntimeError(msg)

    @staticmethod
    def writelog(logfile, contentlist, mode='replace'):
        # type: (AnyStr, Union[AnyStr, List[AnyStr], Tuple[AnyStr]], AnyStr) -> None
        """write log"""
        if logfile is None:  # If logfile is not assigned, just print msg.
            print(UtilClass.print_msg(contentlist))
        else:
            if os.path.exists(logfile):
                if mode == 'replace':
                    os.remove(logfile)
                    log_status = open(logfile, 'w')
                else:
                    log_status = open(logfile, 'a')
            else:
                log_status = open(logfile, 'w')
            log_status.write(UtilClass.print_msg(contentlist))
            log_status.flush()
            log_status.close()

    @staticmethod
    def decode_strs_in_dict(unicode_dict
                            # type: Dict[Union[AnyStr, int], Union[int, float, AnyStr, List[Union[int, float, AnyStr]]]]
                            ):
        # type: (...) -> Dict[Union[AnyStr, int], Any]
        """Decode strings in dictionary which may contains unicode strings or numeric values.

        - 1. integer could be key, float cannot;
        - 2. the function is called recursively

        Examples:
            >>> UtilClass.decode_strs_in_dict({u'1': ['1', 2, 3], u'age': u'28', u'name': u'zhulj'})
            {1: [1, 2, 3], 'age': 28, 'name': 'zhulj'}
            >>> UtilClass.decode_strs_in_dict({u'name': u'zhulj',\
                                               'edu': {'nwsuaf': 2007,\
                                                u'bnu': '2011', 'igsnrr': 2014}})
            {'name': 'zhulj', 'edu': {'nwsuaf': 2007, 'bnu': 2011, 'igsnrr': 2014}}
            >>> UtilClass.decode_strs_in_dict({u'a': ['b', {1: {u'c': 2}}],\
                                               u'd': ('e', {3: {u'f': 4}})})
            {'a': ['b', {1: {'c': 2}}], 'd': ('e', {3: {'f': 4}})}

        """
        unicode_dict = {StringClass.convert_str2num(k): StringClass.convert_str2num(v) for
                        k, v in iteritems(unicode_dict)}
        for k, v in iteritems(unicode_dict):
            if isinstance(v, dict):
                unicode_dict[k] = UtilClass.decode_strs_in_dict(v)
            elif isinstance(v, list):
                unicode_dict[k] = [UtilClass.decode_strs_in_dict(vv) if vv is dict else vv
                                   for vv in v]
            elif isinstance(v, tuple):
                unicode_dict[k] = tuple(UtilClass.decode_strs_in_dict(vvv) if vvv is dict else vvv
                                        for vvv in v)
            else:
                pass
        return unicode_dict


def get_config_file():
    # type: () -> AnyStr
    """Get model configuration file name from argv"""
    parser = argparse.ArgumentParser(description="Read configuration file.")
    parser.add_argument('-ini', help="Full path of configuration file")
    args = parser.parse_args()
    ini_file = args.ini
    if not FileClass.is_file_exists(ini_file):
        print("Usage: -ini <full path to the configuration file.>")
        exit(-1)
    return ini_file


def get_config_parser(case_sensitive=False):  # type: (bool) -> ConfigParser
    """Get config parser.

    Args:
        case_sensitive: True means preserve case-sensitive in ConfigParser.
                        https://stackoverflow.com/a/1611877/4837280
    """
    cf = ConfigParser()
    if case_sensitive:
        cf.optionxform = str
    ini_file = get_config_file()
    cf.read(ini_file)
    return cf


if __name__ == '__main__':
    # Run doctest in docstrings of Google code style
    # python -m doctest utils.py (only when doctest.ELLIPSIS is not specified)
    # or python utils.py -v
    # or py.test --doctest-modules utils.py
    import doctest

    doctest.testmod()
