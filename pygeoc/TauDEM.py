#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""TauDEM Utility Class.

   Thanks to the open-source software `TauDEM`_ by David Tarboton and `QSWAT`_ by Chris George.

   @author: Liangjun Zhu

   @changlog: 12-04-12 jz - origin version.\n
              16-07-01 lj - reorganized for pygeoc.\n
              17-06-25 lj - check by pylint and reformat by Google style.\n

   .. _TauDEM:
      https://github.com/dtarb/TauDEM
   .. _QSWAT:
      http://swat.tamu.edu/software/qswat/
"""

import os

from pygeoc.postTauDEM import DinfUtil
from pygeoc.raster import RasterUtilClass
from pygeoc.utils import UtilClass, MathClass, FileClass, StringClass


class TauDEMFilesUtils(object):
    """predefined TauDEM resulted file names"""
    # intermediate data
    _FILLEDDEM = 'demFilledTau.tif'
    _D8FLOWDIR = 'flowDirTauD8.tif'
    _SLOPE = 'slopeTau.tif'
    _D8ACC = 'accTauD8.tif'
    _D8ACCWITHWEIGHT = 'accTauD8WithWeight.tif'
    _STREAMRASTER = 'streamRasterTau.tif'
    _FLOWDIRDINF = 'flowDirDinfTau.tif'
    _DIRCODEDINF = 'dirCodeDinfTau.tif'
    _WEIGHTDINF = 'weightDinfTau.tif'
    _SLOPEDINF = 'slopeDinfTau.tif'
    _DEFAULTOUTLET = 'outlet_pre.shp'
    _MODIFIEDOUTLET = 'outletM.shp'
    _STREAMSKELETON = 'streamSkeleton.tif'
    _DROPTXT = 'drp.txt'
    _STREAMORDER = 'streamOrderTau.tif'
    _CHNETWORK = 'chNetwork.txt'
    _CHCOORD = 'chCoord.txt'
    _STREAMNET = 'streamNet.shp'
    _DIST2STREAMD8 = 'dist2StreamD8Org.tif'
    _SUBBASIN = 'subbasinTau.tif'
    # masked file names
    _SUBBASINM = 'subbasinTauM.tif'
    _D8FLOWDIRM = 'flowDirTauM.tif'
    _STREAMRASTERM = 'streamRasterTauM.tif'

    def __init__(self, tau_dir):
        """assign taudem resulted file path"""
        tau_dir = os.path.abspath(tau_dir)
        self.workspace = tau_dir
        self.filldem = tau_dir + os.sep + self._FILLEDDEM
        self.d8flow = tau_dir + os.sep + self._D8FLOWDIR
        self.slp = tau_dir + os.sep + self._SLOPE
        self.d8acc = tau_dir + os.sep + self._D8ACC
        self.d8acc_weight = tau_dir + os.sep + self._D8ACCWITHWEIGHT
        self.stream_raster = tau_dir + os.sep + self._STREAMRASTER
        self.dinf = tau_dir + os.sep + self._FLOWDIRDINF
        self.dinf_d8dir = tau_dir + os.sep + self._DIRCODEDINF
        self.dinf_weight = tau_dir + os.sep + self._WEIGHTDINF
        self.dinf_slp = tau_dir + os.sep + self._SLOPEDINF
        self.outlet_pre = tau_dir + os.sep + self._DEFAULTOUTLET
        self.outlet_m = tau_dir + os.sep + self._MODIFIEDOUTLET
        self.stream_pd = tau_dir + os.sep + self._STREAMSKELETON
        self.stream_order = tau_dir + os.sep + self._STREAMORDER
        self.channel_net = tau_dir + os.sep + self._CHNETWORK
        self.channel_coord = tau_dir + os.sep + self._CHCOORD
        self.streamnet_shp = tau_dir + os.sep + self._STREAMNET
        self.dist2stream_d8 = tau_dir + os.sep + self._DIST2STREAMD8
        self.subbsn = tau_dir + os.sep + self._SUBBASIN
        self.subbsn_m = tau_dir + os.sep + self._SUBBASINM
        self.d8flow_m = tau_dir + os.sep + self._D8FLOWDIRM
        self.stream_m = tau_dir + os.sep + self._STREAMRASTERM
        self.drptxt = tau_dir + os.sep + self._DROPTXT


class TauDEM(object):
    """Methods for calling TauDEM executables."""

    def __init__(self):
        """Empty function"""
        pass

    @staticmethod
    def error(msg, log_file=None):
        """Print, output error message and raise RuntimeError."""
        UtilClass.print_msg(msg + os.linesep)
        if log_file is not None:
            UtilClass.writelog(log_file, msg, 'append')
        raise RuntimeError(msg)

    @staticmethod
    def log(lines, log_file=None):
        """Output log message."""
        err = False
        for line in lines:
            print (line)
            if log_file is not None:
                UtilClass.writelog(log_file, line, 'append')
            if 'BAD TERMINATION' in line.upper():
                err = True
                break
        if err:
            TauDEM.error("Error occurred when calling TauDEM function, please check!", log_file)

    @staticmethod
    def run(function_name, in_files, wp=None, in_params=None, out_files=None, mpi_params=None,
            log_params=None):
        """
        Run TauDEM function.

           1. The command will not execute if any input file does not exist.
           2. An error will be detected after running the TauDEM command if
           any output file does not exist;

        Args:
            function_name (str): Full path of TauDEM function.
            in_files (dict, required): Dict of pairs of parameter id (string) and file path
                (string or list) for input files, e.g.::

                    {'-z': '/full/path/to/dem.tif'}

            wp (str, optional): Workspace for outputs. If not specified, the directory of the
                first input file in ``in_files`` will be used.
            in_params (dict, optional): Dict of pairs of parameter id (string) and value
                (or None for a flag parameter without a value) for input parameters, e.g.::

                    {'-nc': None}
                    {'-thresh': threshold}
                    {'-m': 'ave' 's', '-nc': None}

            out_files (dict, optional): Dict of pairs of parameter id (string) and file
                path (string) for output files, e.g.::

                    {'-fel': 'filleddem.tif'}

            mpi_params (dict, optional): Dict of pairs of parameter id (string) and value or
                path for MPI setting, e.g.::

                    {'mpipath':'/soft/bin','hostfile':'/soft/bin/cluster.node','n':4}
                    {'mpipath':'/soft/bin', 'n':4}
                    {'n':4}

            log_params (dict, optional): Dict of pairs of parameter id (string) and value or
                path for runtime and log output parameters. e.g.::

                    {'logfile': '/home/user/log.txt'}

        Returns:
            True if TauDEM run successfully, otherwise False.
        """

        def check_infile_and_wp(curinf, curwp):
            """Check the existance of the given file and directory path.
               1. Raise Runtime exception of both not existed.
               2. If the ``curwp`` is None, the set the base folder of ``curinf`` to it.

            """
            if not os.path.exists(curinf):
                if curwp is None:
                    TauDEM.error('You must specify one of the workspace and the '
                                 'full path of input file!')
                curinf = curwp + os.sep + curinf
                curinf = os.path.abspath(curinf)
                if not os.path.exists(curinf):
                    TauDEM.error('Input files parameter %s is not existed!' % curinf)
            else:
                curinf = os.path.abspath(curinf)
                if curwp is None:
                    curwp = os.path.dirname(curinf)
            return curinf, curwp

        # Check input files
        if in_files is None:
            TauDEM.error('Input files parameter is required!')
        if not isinstance(in_files, dict):
            TauDEM.error('The input files parameter must be a dict!')
        for (pid, infile) in in_files.items():
            if infile is None:
                continue
            if isinstance(infile, list) or isinstance(infile, tuple):
                for idx, inf in enumerate(infile):
                    if inf is None:
                        continue
                    inf, wp = check_infile_and_wp(inf, wp)
                    in_files[pid][idx] = inf
                continue
            if os.path.exists(infile):
                infile, wp = check_infile_and_wp(infile, wp)
                in_files[pid] = os.path.abspath(infile)
            else:
                # For more flexible input files extension.
                # e.g., -inputtags 1 <path/to/tag1.tif> 2 <path/to/tag2.tif> ...
                # in such unpredictable circumstance, we cannot check the existance of
                # input files, so the developer will check it in other place.
                if len(StringClass.split_string(infile, ' ')) > 1:
                    continue
                else:  # the infile still should be a existing file, so check in workspace
                    if wp is None:
                        TauDEM.error('Workspace should not be None!')
                    infile = wp + os.sep + infile
                    if not os.path.exists(infile):
                        TauDEM.error('Input files parameter %s: %s is not existed!' %
                                     (pid, infile))
                    in_files[pid] = os.path.abspath(infile)
        # Make workspace dir if not existed
        UtilClass.mkdir(wp)
        # Check the log parameter
        log_file = None
        if log_params is not None:
            if not isinstance(log_params, dict):
                TauDEM.error('The log parameter must be a dict!')
            if 'logfile' in log_params and log_params['logfile'] is not None:
                log_file = log_params['logfile']
                # If log_file is just a file name, then save it in the default workspace.
                if os.sep not in log_file:
                    log_file = wp + os.sep + log_file
                    log_file = os.path.abspath(log_file)
        # remove out_files to avoid any file IO related error
        new_out_files = list()
        if out_files is not None:
            if not isinstance(out_files, dict):
                TauDEM.error('The output files parameter must be a dict!')
            for (pid, out_file) in out_files.items():
                if out_file is None:
                    continue
                if isinstance(out_file, list) or isinstance(out_file, tuple):
                    for idx, outf in enumerate(out_file):
                        if outf is None:
                            continue
                        outf = FileClass.get_file_fullpath(outf, wp)
                        FileClass.remove_files(outf)
                        out_files[pid][idx] = outf
                        new_out_files.append(outf)
                else:
                    out_file = FileClass.get_file_fullpath(out_file, wp)
                    FileClass.remove_files(out_file)
                    out_files[pid] = out_file
                new_out_files.append(out_file)

        # concatenate command line
        commands = list()
        # MPI header
        if mpi_params is not None:
            if not isinstance(mpi_params, dict):
                TauDEM.error('The MPI settings parameter must be a dict!')
            if 'mpipath' in mpi_params and mpi_params['mpipath'] is not None:
                commands.append(mpi_params['mpipath'] + os.sep + 'mpiexec')
            else:
                commands.append('mpiexec')
            if 'hostfile' in mpi_params and mpi_params['hostfile'] is not None \
                    and not StringClass.string_match(mpi_params['hostfile'], 'none') \
                    and os.path.isfile(mpi_params['hostfile']):
                commands.append('-f')
                commands.append(mpi_params['hostfile'])
            if 'n' in mpi_params and mpi_params['n'] > 1:
                commands.append('-n')
                commands.append(str(mpi_params['n']))
            else:  # If number of processor is less equal than 1, then do not call mpiexec.
                commands = []
        # append TauDEM function name, which can be full path or just one name
        commands.append(function_name)
        # append input files
        for (pid, infile) in in_files.items():
            if infile is None:
                continue
            if pid[0] != '-':
                pid = '-' + pid
            commands.append(pid)
            if isinstance(infile, list) or isinstance(infile, tuple):
                commands.append(' '.join(tmpf for tmpf in infile))
            else:
                commands.append(infile)
        # append input parameters
        if in_params is not None:
            if not isinstance(in_params, dict):
                TauDEM.error('The input parameters must be a dict!')
            for (pid, v) in in_params.items():
                if pid[0] != '-':
                    pid = '-' + pid
                commands.append(pid)
                # allow for parameter which is an flag without value
                if v != '' and v is not None:
                    if MathClass.isnumerical(v):
                        commands.append(str(v))
                    else:
                        commands.append(v)
        # append output parameters
        if out_files is not None:
            for (pid, outfile) in out_files.items():
                if outfile is None:
                    continue
                if pid[0] != '-':
                    pid = '-' + pid
                commands.append(pid)
                if isinstance(outfile, list) or isinstance(outfile, tuple):
                    commands.append(' '.join(tmpf for tmpf in outfile))
                else:
                    commands.append(outfile)
        # run command
        runmsg = UtilClass.run_command(commands)
        TauDEM.log(runmsg, log_file)
        # Check out_files, raise RuntimeError if not exist.
        for of in new_out_files:
            if not os.path.exists(of):
                TauDEM.error('%s failed, and the %s was not generated!' % (function_name, of))
                return False
        return True

    @staticmethod
    def pitremove(np, dem, filleddem, workingdir=None, mpiexedir=None, exedir=None, log_file=None,
                  hostfile=None):
        """Run pit remove using the flooding approach """
        return TauDEM.run(FileClass.get_executable_fullpath('pitremove', exedir),
                          {'-z': dem}, workingdir,
                          None,
                          {'-fel': filleddem},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def d8flowdir(np, filleddem, flowdir, slope, workingdir=None, mpiexedir=None, exedir=None,
                  log_file=None, hostfile=None):
        """Run D8 flow direction"""
        return TauDEM.run(FileClass.get_executable_fullpath('d8flowdir', exedir),
                          {'-fel': filleddem}, workingdir,
                          None,
                          {'-p': flowdir, '-sd8': slope},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def dinfflowdir(np, filleddem, flowangle, slope, workingdir=None, mpiexedir=None, exedir=None,
                    log_file=None, hostfile=None):
        """Run Dinf flow direction"""
        return TauDEM.run(FileClass.get_executable_fullpath('dinfflowdir', exedir),
                          {'-fel': filleddem}, workingdir,
                          None,
                          {'-ang': flowangle, '-slp': slope},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def aread8(np, flowdir, acc, outlet=None, streamskeleton=None, edgecontaimination=False,
               workingdir=None, mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run Accumulate area according to D8 flow direction"""
        # -nc means do not consider edge contaimination
        if not edgecontaimination:
            in_params = {'-nc': None}
        else:
            in_params = None
        return TauDEM.run(FileClass.get_executable_fullpath('aread8', exedir),
                          {'-p': flowdir, '-o': outlet, '-wg': streamskeleton}, workingdir,
                          in_params,
                          {'-ad8': acc},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def areadinf(np, angfile, sca, outlet=None, wg=None, edgecontaimination=False,
                 workingdir=None, mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run Accumulate area according to Dinf flow direction"""
        # -nc means do not consider edge contaimination
        if edgecontaimination:
            in_params = {'-nc': None}
        else:
            in_params = None
        return TauDEM.run(FileClass.get_executable_fullpath('areadinf', exedir),
                          {'-ang': angfile, '-o': outlet, '-wg': wg}, workingdir,
                          in_params,
                          {'-sca': sca},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def connectdown(np, acc, outlet, wtsd=None, workingdir=None, mpiexedir=None,
                    exedir=None, log_file=None, hostfile=None):
        """Reads an ad8 contributing area file,
        identifies the location of the largest ad8 value as the outlet of the largest watershed"""
        # if wtsd is None or os.path.exists(wtsd):

        return TauDEM.run(FileClass.get_executable_fullpath('connectdown', exedir),
                          {'-ad8': acc, '-w': wtsd},
                          workingdir,
                          None,
                          {'-o': outlet},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def gridnet(np, pfile, plenfile, tlenfile, gordfile, outlet=None, workingdir=None,
                mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run gridnet"""
        return TauDEM.run(FileClass.get_executable_fullpath('gridnet', exedir),
                          {'-p': pfile, '-o': outlet}, workingdir,
                          None,
                          {'-plen': plenfile, '-tlen': tlenfile, '-gord': gordfile},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def threshold(np, acc, stream_raster, threshold=100., workingdir=None,
                  mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run threshold for stream raster"""
        return TauDEM.run(FileClass.get_executable_fullpath('threshold', exedir),
                          {'-ssa': acc}, workingdir,
                          {'-thresh': threshold},
                          {'-src': stream_raster},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def streamnet(np, filleddem, flowdir, acc, streamRaster, modifiedOutlet,
                  streamOrder, chNetwork, chCoord, streamNet, subbasin, workingdir=None,
                  mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run streamnet"""
        return TauDEM.run(FileClass.get_executable_fullpath('streamnet', exedir),
                          {'-fel': filleddem, '-p': flowdir, '-ad8': acc, '-src': streamRaster,
                           '-o': modifiedOutlet}, workingdir,
                          None,
                          {'-ord': streamOrder, '-tree': chNetwork, '-coord': chCoord,
                           '-net': streamNet, '-w': subbasin},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def moveoutletstostrm(np, flowdir, streamRaster, outlet, modifiedOutlet,
                          workingdir=None, mpiexedir=None,
                          exedir=None, log_file=None, hostfile=None):
        """Run move the given outlets to stream"""
        return TauDEM.run(FileClass.get_executable_fullpath('moveoutletstostrm', exedir),
                          {'-p': flowdir, '-src': streamRaster, '-o': outlet},
                          workingdir,
                          None,
                          {'-om': modifiedOutlet},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def convertdistmethod(method_str):
        """Convert distance method to h, v, p, and s."""
        if StringClass.string_match(method_str, 'Horizontal'):
            return 'h'
        elif StringClass.string_match(method_str, 'Vertical'):
            return 'v'
        elif StringClass.string_match(method_str, 'Pythagoras'):
            return 'p'
        elif StringClass.string_match(method_str, 'Surface'):
            return 's'
        elif method_str.lower() in ['h', 'v', 'p', 's']:
            return method_str.lower()
        else:
            return 's'

    @staticmethod
    def convertstatsmethod(method_str):
        """Convert statistics method to ave, min, and max."""
        if StringClass.string_match(method_str, 'Average'):
            return 'ave'
        elif StringClass.string_match(method_str, 'Maximum'):
            return 'max'
        elif StringClass.string_match(method_str, 'Minimum'):
            return 'min'
        elif method_str.lower() in ['ave', 'max', 'min']:
            return method_str.lower()
        else:
            return 'ave'

    @staticmethod
    def d8hdisttostrm(np, p, fel, src, dist, thresh, workingdir=None,
                      mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run D8 distance down to stream.
        """
        return TauDEM.run(FileClass.get_executable_fullpath('d8hdisttostrm', exedir),
                          {'-fel': fel, '-p': p, '-src': src},
                          workingdir,
                          {'-thresh': thresh},
                          {'-dist': dist},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def d8distdowntostream(np, p, fel, src, dist, distancemethod, thresh, workingdir=None,
                           mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run D8 distance down to stream by different method for distance.
        This function is extended from d8hdisttostrm by Liangjun.

        Please clone `TauDEM by lreis2415`_ and compile for this program.

        .. _TauDEM by lreis2415:
           https://github.com/lreis2415/TauDEM
        """
        return TauDEM.run(FileClass.get_executable_fullpath('d8distdowntostream', exedir),
                          {'-fel': fel, '-p': p, '-src': src},
                          workingdir,
                          {'-thresh': thresh, '-m': TauDEM.convertdistmethod(distancemethod)},
                          {'-dist': dist},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def dinfdistdown(np, ang, fel, slp, src, statsm, distm, edgecontamination, wg, dist,
                     workingdir=None, mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run D-inf distance down to stream"""
        in_params = {'-m': '%s %s' % (TauDEM.convertstatsmethod(statsm),
                                      TauDEM.convertdistmethod(distm))}
        if StringClass.string_match(edgecontamination, 'false') or edgecontamination is False:
            in_params['-nc'] = None
        return TauDEM.run(FileClass.get_executable_fullpath('dinfdistdown', exedir),
                          {'-fel': fel, '-slp': slp, '-ang': ang, '-src': src, '-wg': wg},
                          workingdir,
                          in_params,
                          {'-dd': dist},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def peukerdouglas(np, fel, streamSkeleton, workingdir=None, mpiexedir=None, exedir=None,
                      log_file=None, hostfile=None):
        """Run peuker-douglas function"""
        return TauDEM.run(FileClass.get_executable_fullpath('peukerdouglas', exedir),
                          {'-fel': fel}, workingdir,
                          None,
                          {'-ss': streamSkeleton},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})

    @staticmethod
    def dropanalysis(np, fel, p, ad8, ssa, outlet, minthresh, maxthresh, numthresh,
                     logspace, drp, workingdir=None,
                     mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Drop analysis for optimal threshold for extracting stream."""
        parstr = '%f %f %f' % (minthresh, maxthresh, numthresh)
        if logspace == 'false':
            parstr += ' 1'
        else:
            parstr += ' 0'
        return TauDEM.run(FileClass.get_executable_fullpath('dropanalysis', exedir),
                          {'-fel': fel, '-p': p, '-ad8': ad8, '-ssa': ssa, '-o': outlet},
                          workingdir,
                          {'-par': parstr},
                          {'-drp': drp},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': log_file})


class TauDEMWorkflow(object):
    """Common used workflow based on TauDEM"""

    def __init__(self):
        """Empty function"""
        pass

    @staticmethod
    def watershed_delineation(np, dem, outlet_file=None, thresh=0, singlebasin=False,
                              tau_dir=None, mpi_bin=None, bin_dir=None,
                              logfile=None, hostfile='delineate_wtsd.log'):
        """Watershed Delineation."""
        # 1. Check directories
        if not os.path.exists(dem):
            TauDEM.error('DEM: %s is not existed!' % dem)
        dem = os.path.abspath(dem)
        if tau_dir is None:
            tau_dir = os.path.dirname(dem)
        namecfg = TauDEMFilesUtils(tau_dir)
        tau_dir = namecfg.workspace
        UtilClass.mkdir(tau_dir)
        # 2. Check log file
        if logfile is not None and FileClass.is_file_exists(logfile):
            os.remove(logfile)
        # 3. Get predefined intermediate file names
        filled_dem = namecfg.filldem
        flow_dir = namecfg.d8flow
        slope = namecfg.slp
        flow_dir_dinf = namecfg.dinf
        slope_dinf = namecfg.dinf_slp
        dir_code_dinf = namecfg.dinf_d8dir
        weight_dinf = namecfg.dinf_weight
        acc = namecfg.d8acc
        stream_raster = namecfg.stream_raster
        default_outlet = namecfg.outlet_pre
        modified_outlet = namecfg.outlet_m
        stream_skeleton = namecfg.stream_pd
        acc_with_weight = namecfg.d8acc_weight
        stream_order = namecfg.stream_order
        ch_network = namecfg.channel_net
        ch_coord = namecfg.channel_coord
        stream_net = namecfg.streamnet_shp
        subbasin = namecfg.subbsn
        dist2_stream_d8 = namecfg.dist2stream_d8

        # 4. perform calculation
        UtilClass.writelog(logfile, "[Output] %d..., %s" % (10, "pitremove DEM..."), 'a')
        TauDEM.pitremove(np, dem, filled_dem, tau_dir, mpi_bin, bin_dir,
                         log_file=logfile, hostfile=hostfile)
        UtilClass.writelog(logfile, "[Output] %d..., %s" %
                           (20, "Calculating D8 and Dinf flow direction..."), 'a')
        TauDEM.d8flowdir(np, filled_dem, flow_dir, slope, tau_dir,
                         mpi_bin, bin_dir, log_file=logfile, hostfile=hostfile)
        TauDEM.dinfflowdir(np, filled_dem, flow_dir_dinf, slope_dinf, tau_dir,
                           mpi_bin, bin_dir, log_file=logfile, hostfile=hostfile)
        DinfUtil.output_compressed_dinf(flow_dir_dinf, dir_code_dinf, weight_dinf)
        UtilClass.writelog(logfile, "[Output] %d..., %s" % (30, "D8 flow accumulation..."), 'a')
        TauDEM.aread8(np, flow_dir, acc, None, None, tau_dir, mpi_bin, bin_dir,
                      log_file=logfile, hostfile=hostfile)
        UtilClass.writelog(logfile, "[Output] %d..., %s" %
                           (40, "Generating stream raster initially..."), 'a')
        min_accum, max_accum, mean_accum, std_accum = RasterUtilClass.raster_statistics(acc)
        TauDEM.threshold(np, acc, stream_raster, mean_accum, tau_dir,
                         mpi_bin, bin_dir, log_file=logfile, hostfile=hostfile)
        UtilClass.writelog(logfile, "[Output] %d..., %s" % (50, "Moving outlet to stream..."), 'a')
        if outlet_file is None:
            outlet_file = default_outlet
            TauDEM.connectdown(np, acc, outlet_file, tau_dir, mpi_bin, bin_dir,
                               log_file=logfile, hostfile=hostfile)
        TauDEM.moveoutletstostrm(np, flow_dir, stream_raster, outlet_file,
                                 modified_outlet, tau_dir, mpi_bin, bin_dir,
                                 log_file=logfile, hostfile=hostfile)
        UtilClass.writelog(logfile, "[Output] %d..., %s" %
                           (60, "Generating stream skeleton..."), 'a')
        TauDEM.peukerdouglas(np, filled_dem, stream_skeleton, tau_dir,
                             mpi_bin, bin_dir, log_file=logfile, hostfile=hostfile)
        UtilClass.writelog(logfile, "[Output] %d..., %s" %
                           (70, "Flow accumulation with outlet..."), 'a')
        tmp_outlet = None
        if singlebasin:
            tmp_outlet = modified_outlet
        TauDEM.aread8(np, flow_dir, acc_with_weight, tmp_outlet, stream_skeleton,
                      tau_dir, mpi_bin, bin_dir, log_file=logfile, hostfile=hostfile)

        if thresh <= 0:  # find the optimal threshold using dropanalysis function
            UtilClass.writelog(logfile, "[Output] %d..., %s" %
                               (75, "Drop analysis to select optimal threshold..."), 'a')
            min_accum, max_accum, mean_accum, std_accum = \
                RasterUtilClass.raster_statistics(acc_with_weight)
            if mean_accum - std_accum < 0:
                minthresh = mean_accum
            else:
                minthresh = mean_accum - std_accum
            maxthresh = mean_accum + std_accum
            numthresh = 20
            logspace = 'true'
            drp_file = namecfg.drptxt
            TauDEM.dropanalysis(np, filled_dem, flow_dir, acc_with_weight,
                                acc_with_weight, modified_outlet, minthresh, maxthresh,
                                numthresh, logspace, drp_file, tau_dir, mpi_bin, bin_dir,
                                log_file=logfile, hostfile=hostfile)
            if not FileClass.is_file_exists(drp_file):
                raise RuntimeError("Dropanalysis failed and drp.txt was not created!")
            drpf = open(drp_file, "r")
            temp_contents = drpf.read()
            (beg, thresh) = temp_contents.rsplit(' ', 1)
            print (thresh)
            drpf.close()
        UtilClass.writelog(logfile, "[Output] %d..., %s" % (80, "Generating stream raster..."), 'a')
        TauDEM.threshold(np, acc_with_weight, stream_raster, float(thresh),
                         tau_dir, mpi_bin, bin_dir, log_file=logfile, hostfile=hostfile)
        UtilClass.writelog(logfile, "[Output] %d..., %s" % (90, "Generating stream net..."), 'a')
        TauDEM.streamnet(np, filled_dem, flow_dir, acc_with_weight, stream_raster,
                         modified_outlet, stream_order, ch_network,
                         ch_coord, stream_net, subbasin, tau_dir, mpi_bin, bin_dir,
                         log_file=logfile, hostfile=hostfile)
        UtilClass.writelog(logfile, "[Output] %d..., %s" %
                           (95, "Calculating distance to stream (D8)..."), 'a')
        TauDEM.d8hdisttostrm(np, flow_dir, filled_dem, stream_raster, dist2_stream_d8, 1,
                             tau_dir, mpi_bin, bin_dir, log_file=logfile, hostfile=hostfile)
        UtilClass.writelog(logfile, "[Output] %d.., %s" %
                           (100, "Original subbasin delineation is finished!"), 'a')


def run_test():
    workingspace = r'../tests/data/tmp_results'
    dem = '../tests/data/Jamaica_dem.tif'
    log = 'taudem.log'
    td_names = TauDEMFilesUtils(workingspace)

    TauDEM.pitremove(1, dem, td_names.filldem, workingspace, log_file=log)
    TauDEM.d8flowdir(4, td_names.filldem, td_names.d8flow, td_names.slp, workingspace, log_file=log)


if __name__ == "__main__":
    run_test()
