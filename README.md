![pygeoc](docs/img/pygeoc.png)

[![Travis branch](https://img.shields.io/travis/lreis2415/PyGeoC/master.svg)](https://travis-ci.org/lreis2415/PyGeoC)
[![Coveralls branch](https://img.shields.io/coveralls/lreis2415/PyGeoC/master.svg)](https://coveralls.io/github/lreis2415/PyGeoC?branch=master)

详情请访问[用户手册及开发文档](https://lreis2415.github.io/PyGeoC/)。

## 依赖
+ Python >= 2.7 (compatible with Python 3)
+ GDAL >=1.9

  详细安装配置请参考[GDAL for Python](docs/python_gdal_install.rst)。
+ Numpy >=1.9
+ [TauDEM 5.3.7+](http://hydrology.usu.edu/taudem/taudem5/)

  用于水文模块。

## 安装
PyGeoC处在不断开发完善中，请根据如下命令安装最新开发版本。

```bash
git clone https://github.com/lreis2415/PyGeoC
cd PyGeoC
sudo ./reinstall.sh (linux)
./reinstall.bat (windows, open cmd as Administrator)
```

