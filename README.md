![pygeoc](docs/img/pygeoc.png)

[![Build Status](https://travis-ci.org/lreis2415/PyGeoC.svg?branch=master)](https://travis-ci.org/lreis2415/PyGeoC)
[![Coverage Status](https://coveralls.io/repos/github/lreis2415/PyGeoC/badge.svg)](https://coveralls.io/github/lreis2415/PyGeoC)


## 依赖
+ Python 2.7
+ GDAL >=1.9,<2.0

  详细安装配置请参考[GDAL for Python](docs/python_gdal_install.rst)。
+ Numpy >=1.9

## 安装
PyGeoC处在不断开发完善中，请根据如下命令安装最新开发版本。

```bash
git clone https://github.com/lreis2415/PyGeoC
cd PyGeoC
python setup.py install
```

## 快速开始

+ 1.读取栅格文件
```pydocstring
>>> from pygeoc.raster import RasterUtilClass
>>> input_tif = "../tests/data/Jamaica_dem.tif"
>>> rst = RasterUtilClass.read_raster(input_tif)
>>> # rst 为pygeoc.raster.Raster类，可访问栅格元数据或简单统计信息
>>> print ("rows: %d, cols: %d" % (rst.nRows, rst.nCols))
>>> print ("LLCornerX: %f, LLCornerY: %f" % (rst.xMin, rst.yMin))
>>> print ("cell size: %f" % rst.dx)
>>> print ("mean: %f, max: %f, min: %f" % (rst.get_average(), rst.get_max(), rst.get_min()))
>>> print ("std: %f, sum: %f" % (rst.get_std(), rst.get_sum()))
rows: 130, cols: 100
LLCornerX: 755145.277178, LLCornerY: 654294.061945
cell size: 10.000000
Coornate system: 
mean: 203.920532, max: 284.074493, min: 139.114227
std: 32.323097, sum: 2650967.000000
```
