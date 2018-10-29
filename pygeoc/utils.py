#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility Classes and Functions

    @author: Liangjun Zhu

    @changlog: 12-04-12 jz - origin version.\n
               16-07-01 lj - reorganized for pygeoc.\n
               17-06-25 lj - check by pylint and reformat by Google style.\n
"""
from __future__ import division
from future.utils import iteritems

import argparse
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

import numpy

from configparser import ConfigParser

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
    """
    try:
        from builtins import int
        return isinstance(v, int)  # Match both int and long on Py2
    except ImportError:
        from past.builtins import long
        return isinstance(v, (int, long))


def is_string(in_str):
    """Test Unicode (text) string literal.

    Examples:
        >>> is_string('abc')
        True
        >>> is_string(u'abc')
        True
        >>> is_string(u'北京')
        True

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
        """If float a is equal to float b."""
        return abs(a - b) < DELTA

    @staticmethod
    def nashcoef(obsvalues, simvalues, log=False, expon=2):
        # type: (list, list, bool, float) -> float
        """Calculate Nash-Sutcliffe coefficient(NSE) proposed by
           Nash and Sutcliffe (1970) and its variants.
           The following description is referred by Krause et al. (2005)
             and Moriasi et al. (2007).
           [1] The range of NSE lies between -inf and 1.0 (prefect fit).
           [2] Since the differences between observed and simulated values
               are calculated as squared values (`expon`=2), the larger values
               in a time series are strongly overestimated whereas lower
               values are neglected (Legates and McCabe, 1999). For the
               quantification of runoff prediction, this leads to an overestimation
               of the model performance during peak flows and an underestimation
               during low flow conditions.
           [3] Similar to R-square, NSE is not very sensitive to systematic
               model over- or underestimation especially during low flow periods.
           [4] To reduce the sensitivity of the original NSE to extreme values,
               the NSE is often calculated with logarithmic values of obseravtion
               and simulation values, which known as lnE. As a result, the
               influence of the low flow values is increased in comparison to the
               flood peaks resulting in an increase in sensitivity of lnE to
               systematic model over- or underestimation.
           [5] A more general form could be used for the same purpose as lnE, i.e.,
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
        if len(obsvalues) != len(simvalues):
            raise ValueError("The size of observed and simulated values must be"
                             " the same for NSE calculation!")
        if not isinstance(obsvalues, numpy.ndarray):
            obsvalues = numpy.array(obsvalues)
        if not isinstance(simvalues, numpy.ndarray):
            simvalues = numpy.array(simvalues)
        if log:  # Be care of zero values
            obsvalues = numpy.where((obsvalues == 0.) | (simvalues == 0.), numpy.nan, obsvalues)
            simvalues = numpy.where((obsvalues == 0.) | (simvalues == 0.), numpy.nan, simvalues)
            obsvalues = numpy.log(obsvalues)
            simvalues = numpy.log(simvalues)
        if expon > len(obsvalues) or expon < 1:
            return 0.
        ave = numpy.nanmean(obsvalues)
        a1 = numpy.nansum(numpy.abs(obsvalues - simvalues) ** expon)
        a2 = numpy.nansum(numpy.abs(obsvalues - ave) ** expon)
        if a2 == 0.:
            return 1.
        return 1. - a1 / a2

    @staticmethod
    def rsquare(obsvalues, simvalues):
        # type: (list, list) -> float
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
        if len(obsvalues) != len(simvalues):
            raise ValueError("The size of observed and simulated values must be "
                             "the same for R-square calculation!")
        if not isinstance(obsvalues, numpy.ndarray):
            obsvalues = numpy.array(obsvalues)
        if not isinstance(simvalues, numpy.ndarray):
            simvalues = numpy.array(simvalues)
        obs_avg = numpy.mean(obsvalues)
        pred_avg = numpy.mean(simvalues)
        obs_minus_avg_sq = numpy.sum((obsvalues - obs_avg) ** 2)
        pred_minus_avg_sq = numpy.sum((simvalues - pred_avg) ** 2)
        obs_pred_minus_avgs = numpy.sum((obsvalues - obs_avg) * (simvalues - pred_avg))
        # Calculate R-square
        yy = obs_minus_avg_sq ** 0.5 * pred_minus_avg_sq ** 0.5
        if yy == 0.:
            return 1.
        return (obs_pred_minus_avgs / yy) ** 2.

    @staticmethod
    def rmse(obsvalues, simvalues):
        # type: (list, list) -> float
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
        if len(obsvalues) != len(simvalues):
            raise ValueError("The size of observed and simulated values must be "
                             "the same for R-square calculation!")
        if not isinstance(obsvalues, numpy.ndarray):
            obsvalues = numpy.array(obsvalues)
        if not isinstance(simvalues, numpy.ndarray):
            simvalues = numpy.array(simvalues)
        return numpy.sqrt(numpy.mean((obsvalues - simvalues) ** 2.))

    @staticmethod
    def pbias(obsvalues, simvalues):
        # type: (list, list) -> float
        """Calculate PBIAS, or percent model bias.

        Args:
            obsvalues: observe values array
            simvalues: simulate values array

        Examples:
            >>> obs = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96,\
                       4.00, 2.24, 29.28, 5.88, 0.86, 13.21]
            >>> sim = [2.90, 2.87, 2.85, 2.83, 3.04, 2.81, 2.85,\
                       2.78, 2.76, 13.40, 2.70, 2.09, 1.62]
            >>> MathClass.pbias(obs, sim)  # doctest: +ELLIPSIS
            35.46099290780142...

        Returns:
            PBIAS value (percentage), or raise exception
        """
        if len(obsvalues) != len(simvalues):
            raise ValueError("The size of observed and simulated values must be"
                             " the same for PBIAS calculation!")
        return sum(map(lambda x, y: (x - y) * 100, obsvalues, simvalues)) / sum(obsvalues)

    @staticmethod
    def rsr(obsvalues, simvalues):
        # type: (list, list) -> float
        """Calculate RSR (RMSE-to-SD Ratio).

        Programmed according to equation (3) in
        Moriasi et al. 2007.  Model evalutaion guidelines for systematic quantification of accuracy 
          in watershed simulations.  Transactions of the ASABE 50(3): 885-900.

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
        if len(obsvalues) != len(simvalues):
            raise ValueError("The size of observed and simulated values must be"
                             " the same for RSR calculation!")
        mean_obs = sum(obsvalues) / len(obsvalues)
        return sqrt(sum(map(lambda x, y: (x - y) ** 2, obsvalues, simvalues))) / \
               sqrt(sum(map(lambda x, y: (x - y) ** 2, obsvalues, [mean_obs] * len(obsvalues))))


class StringClass(object):
    """String handling class
    """

    def __init__(self):
        """Empty"""
        pass

    @staticmethod
    def convert_unicode2str(unicode_str):
        """convert the input string or string list which is unicode to string.

        Examples:
            >>> StringClass.convert_unicode2str(u'unicode_str')
            'unicode_str'
            >>> StringClass.convert_unicode2str('normal_str')
            'normal_str'
        """
        if is_string(unicode_str):
            return StringClass.convert_unicode2str_num(unicode_str)
        elif isinstance(unicode_str, tuple) or isinstance(unicode_str, list):
            return [StringClass.convert_unicode2str_num(v) for v in unicode_str]
        else:  # if not supported, return what it is
            return unicode_str

    @staticmethod
    def convert_unicode2str_num(unicode_str):
        """Convert unicode string to string, integer, or float."""
        if is_string(unicode_str):
            unicode_str = str(unicode_str)
        if MathClass.isnumerical(unicode_str):
            unicode_str = float(unicode_str)
            if unicode_str % 1. == 0.:
                unicode_str = int(unicode_str)
        return unicode_str

    @staticmethod
    def string_match(str1, str2):
        """Compare two string regardless capital or not"""
        return str1.lower() == str2.lower()

    @staticmethod
    def split_string(str_src, spliters=None, elim_empty=False):
        """Split string by split character space(' ') and indent('\t') as default
        Args:
            str_src: source string
            spliters: e.g. [' ', '\t'], []
            elim_empty: Eliminate empty (i.e., '') or not.

        Returns:
            split sub-strings as list
        """
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
        """Is substr part of str_src, case insensitive."""
        return substr.lower() in str_src.lower()

    @staticmethod
    def string_in_list(tmp_str, strlist):
        """Is tmp_str in strlist, case insensitive."""
        new_str_list = strlist[:]
        for i, str_in_list in enumerate(new_str_list):
            new_str_list[i] = str_in_list.lower()
        return tmp_str.lower() in new_str_list

    @staticmethod
    def is_valid_ip_addr(address):
        """Check the validation of IP address"""
        try:
            socket.inet_aton(address)
            return True
        except Exception:
            return False

    @staticmethod
    def extract_numeric_values_from_string(str_contains_values):
        """
        Find numeric values from string, e.g., 1, .7, 1.2, 4e2, 3e-3, -9, etc.
        reference: https://stackoverflow.com/questions/4703390/
                           how-to-extract-a-floating-number-from-a-string-in-python/4703508#4703508
        Examples:
            ".1 .12 9.1 98.1 1. 12. 1 12" ==> [0.1, 0.12, 9.1, 98.1, 1.0, 12.0, 1.0, 12.0]
            "-1 +1 2e9 +2E+09 -2e-9" ==> [-1.0, 1.0, 2000000000.0, 2000000000.0, -2e-09]
            "current level: -2.03e+99db" ==> [-2.03e+99]
        Args:
            str_contains_values: string which may contains numeric values

        Returns:
            list of numeric values
        """
        numeric_const_pattern = r'[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?'
        rx = re.compile(numeric_const_pattern, re.VERBOSE)
        value_strs = rx.findall(str_contains_values)
        if len(value_strs) == 0:
            return None
        else:
            return [float(v) for v in value_strs]

    @staticmethod
    def get_datetime(formatted_str, user_fmt=None):
        """get datetime() object from string formatted %Y-%m-%d %H:%M:%S"""
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
        """Check the existence of file path."""
        if filename is None or not os.path.exists(filename) or not os.path.isfile(filename):
            return False
        else:
            return True

    @staticmethod
    def is_dir_exists(dirpath):
        """Check the existence of folder path."""
        if dirpath is None or not os.path.exists(dirpath) or not os.path.isdir(dirpath):
            return False
        else:
            return True

    @staticmethod
    def check_file_exists(filename):
        """Throw exception if the file not existed"""
        if not FileClass.is_file_exists(filename):
            UtilClass.error("Input files path %s is None or not existed!\n" % filename)

    @staticmethod
    def copy_files(filename, dstfilename):
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
        """
        Delete all files with same root as fileName,
        i.e. regardless of suffix, such as ESRI shapefile
        """
        pattern = os.path.splitext(filename)[0] + '.*'
        for f in glob.iglob(pattern):
            os.remove(f)

    @staticmethod
    def is_up_to_date(outfile, basedatetime):
        """Return true if outfile exists and is no older than base datetime."""
        if os.path.exists(outfile):
            if os.path.getmtime(outfile) >= basedatetime:
                return True
        return False

    @staticmethod
    def get_executable_fullpath(name, dirname=None):
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
            findout = UtilClass.run_command('where %s' % name)
        else:
            findout = UtilClass.run_command('which %s' % name)
        if not findout or len(findout) == 0:
            print("%s is not included in the env path" % name)
            exit(-1)
        first_path = findout[0].split('\n')[0]
        if os.path.exists(first_path):
            return first_path
        return None

    @staticmethod
    def get_file_fullpath(name, dirname=None):
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
    def get_filename_by_suffixes(dir_src, suffixes):
        """get file names with the given suffixes in the given directory
        Args:
            dir_src: directory path
            suffixes: wanted suffixes list, the suffix in suffixes can with or without '.'

        Returns:
            file names with the given suffixes as list
        """
        list_files = os.listdir(dir_src)
        re_files = list()
        if not isinstance(suffixes, list):
            suffixes = [suffixes]
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
        """get full file names with the given suffixes in the given directory
        Args:
            dir_src: directory path
            suffixes: wanted suffixes

        Returns:
            full file names with the given suffixes as list
        """
        full_paths = list()
        for name in FileClass.get_filename_by_suffixes(dir_src, suffixes):
            full_paths.append(dir_src + os.sep + name)
        return full_paths

    @staticmethod
    def get_core_name_without_suffix(file_path):
        """Return core file name without suffix.

        Examples:
            >>> FileClass.get_core_name_without_suffix(r'/home/zhulj/1990.01.30/test.01.tif')
            'test.01'
            >>> FileClass.get_core_name_without_suffix(r'C:\zhulj\igsnrr\lreis.txt')
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
        """Add postfix for a full file path.

        Examples:
            input: '/home/zhulj/dem.tif', 'filled'
            output: '/home/zhulj/dem_filled.tif'
        """
        corename = FileClass.get_core_name_without_suffix(file_path)
        suffix = os.path.basename(file_path).split('.')[-1]
        return os.path.dirname(file_path) + os.sep + corename + '_' + postfix + '.' + suffix


class DateClass(object):
    """Utility function to handle datetime."""

    def __init__(self):
        """Empty"""
        pass

    @staticmethod
    def is_leapyear(year):
        """Is leap year?"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @staticmethod
    def day_of_month(year, month):
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
    def run_command(commands):
        """Execute external command, and return the output lines list
        17-07-04 lj - Handling subprocess crash in Windows, refers to
            https://stackoverflow.com/questions/5069224/handling-subprocess-crash-in-windows
        Args:
            commands: string or list

        Returns:
            output lines
        """
        commands = StringClass.convert_unicode2str(commands)
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
        process = subprocess.Popen(commands, shell=use_shell, stdout=subprocess.PIPE,
                                   stdin=open(os.devnull),
                                   stderr=subprocess.STDOUT, universal_newlines=True,
                                   startupinfo=startupinfo,
                                   creationflags=subprocess_flags)
        out, err = process.communicate()
        recode = process.returncode

        if out is None:
            return ['']
        if recode is not None and recode != 0:
            raise subprocess.CalledProcessError(-1, commands,
                                                "ERROR occurred when running subprocess!")
        if '\n' in out:
            return out.split('\n')

        return [out]

    @staticmethod
    def current_path(local_function):
        """Get current path
        Reference: https://stackoverflow.com/questions/2632199/how-do-i-get-the-path-of-the-current-executed-file-in-python/18489147#18489147
        Examples:
            from pygeoc.utils import UtilClass
            curpath = UtilClass.current_path(lambda: 0)
        """
        from inspect import getsourcefile
        fpath = getsourcefile(local_function)
        if fpath is None:
            return None
        return os.path.dirname(os.path.abspath(fpath))

    @staticmethod
    def mkdir(dir_path):
        """Make directory if not existed"""
        if not os.path.isdir(dir_path) or not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def rmmkdir(dir_path):
        """If directory existed, then remove and make; else make it."""
        if not os.path.isdir(dir_path) or not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            rmtree(dir_path, True)
            os.makedirs(dir_path)

    @staticmethod
    def print_msg(contentlist):
        """concatenate message list as single string"""
        if isinstance(contentlist, list) or isinstance(contentlist, tuple):
            contentstr = ''
            for content in contentlist:
                contentstr += '%s\n' % content
            return contentstr
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
    def decode_strs_in_dict(unicode_dict):
        """
        Decode strings in dictionary which may contains unicode.
        1. integer could be key, float cannot;\n
        2. the function is called recursively
        Args:
            unicode_dict: {u'name': u'zhulj', u'age': u'26', u'1': [1, 2, 3]}

        Returns:
            decoded dict: {'name': 'zhulj', 'age': 26, 1: [1, 2, 3]}
        """
        unicode_dict = {StringClass.convert_unicode2str(k): StringClass.convert_unicode2str(v) for
                        k, v in iteritems(unicode_dict)}
        for k, v in iteritems(unicode_dict):
            if isinstance(v, dict):
                unicode_dict[k] = UtilClass.decode_strs_in_dict(v)
        return unicode_dict


def get_config_file():
    """Get model configuration file name from argv"""
    parser = argparse.ArgumentParser(description="Read configuration file.")
    parser.add_argument('-ini', help="Full path of configuration file")
    args = parser.parse_args()
    ini_file = args.ini
    if not FileClass.is_file_exists(ini_file):
        print("Usage: -ini <full path to the configuration file.>")
        exit(-1)
    return ini_file


def get_config_parser():
    """Get config parser."""
    cf = ConfigParser()
    ini_file = get_config_file()
    cf.read(ini_file)
    return cf


if __name__ == '__main__':
    # Run doctest in docstrings of Google code style
    # python -m doctest utils.py (only when doctest.ELLIPSIS is not specified)
    # or python utils.py -v
    # or py.test --doctest-module utils.py
    import doctest

    doctest.testmod()
