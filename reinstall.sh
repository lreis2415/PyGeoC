#!/usr/bin/env bash
#
#    This file is aimed for reCompile and reInstall PyGeoC for debugging on Linu/Unix platform.
#
cd $PWD
rm -r dist
rm -r build
python -m pip install tox
python setup.py bdist_wheel --python-tag py2
cd dist
if python -c "import pygeoc" &> /dev/null; then
    echo 'PyGeoC has been installed, and will be uninstalled first.'
    python -m pip uninstall PyGeoC
else
    echo 'PyGeoC will be firstly installed.'
fi
for i in `find . -name *.whl`; do python -m pip install $i --upgrade; done