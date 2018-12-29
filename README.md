![pygeoc](docs/img/pygeoc.png)

[![Travis branch](https://img.shields.io/travis/lreis2415/PyGeoC/master.svg)](https://travis-ci.org/lreis2415/PyGeoC)
[![Coveralls branch](https://img.shields.io/coveralls/lreis2415/PyGeoC/master.svg)](https://coveralls.io/github/lreis2415/PyGeoC?branch=master)

详情请访问[用户手册及开发文档](https://lreis2415.github.io/PyGeoC/)。

## 依赖
+ Python >= 2.7 (compatible with Python 3)
+ GDAL >=1.9
+ Numpy >=1.9
+ matplotlib
+ [TauDEM 5.3.7+](http://hydrology.usu.edu/taudem/taudem5/)

  用于水文模块。

## 安装

### GDAL and numpy
Although the GISInternals support site (http://www.gisinternals.com/index.html) also provides the GDAL Python bindings (e.g., GDAL-1.11.4.win-amd64-py2.7.msi), it may not work properly. So, the site of Unofficial Windows Binaries for Python Extension Packages by Christoph Gohlke (https://www.lfd.uci.edu/~gohlke/pythonlibs/) is highly recommended. Not only the GDAL, almost the commonly used packages can be found here.
Please read the instructions very carefully at the head of this website.
+ Select 32- or 64-bit binaries of packages according to the version of your python, not the version of your Windows. In other words, even if the Windows is 64-bit, the Python can be 32- or 64-bit.
+ Install Microsoft Visual C++ Redistributable packages first, since many binaries cannot run without them, i.e., Microsoft Visual C++ 2008 (x64, x86, and SP1 for CPython 2.7), Visual C++ 2010 (x64 and x86 for CPython 3.4), or the Visual C++ 2017 (x64 or x86 for CPython 3.5, 3.6, and 3.7).
+ Install numpy+mkl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy), e.g., numpy-1.15.4+mkl-cp27-cp27m-win_amd64.whl.
 
+ Install GDAL (https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal), e.g. GDAL-2.2.4-cp27-cp27m-win_amd64.whl. 
 
+ (Optional) Install Esri’s FileGDB API 1.3 or FileGDB 1.5 if you want to use the FileGDB plugin for GDAL. Otherwise, just delete the ogr_FileGDB.dll located in D:\demo\python27\Lib\site-packages\osgeo\gdalplugins.
+ Open a CMD window and enter the following commands to test if the GDAL package for Python is successfully installed.

### Install PyGeoC

PyGeoC处在不断开发完善中，请根据如下命令安装最新开发版本。

```bash
git clone https://github.com/lreis2415/PyGeoC
cd PyGeoC
# For *nix OS
sudo ./reinstall.sh
# For Windows, open a cmd windows as Administrator
./reinstall.bat
# You can specific the Python path, e.g.,
./reinstall.bat D:\demo\python36
```

### For Developers

```bash
pip install -r requirements_dev.txt
```