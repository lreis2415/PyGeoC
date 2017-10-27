#!/usr/bin/env bash
#
#    This file is aimed for reCompile and reInstall PyGeoC for debugging on Linu/Unix platform.
#
#    PyGeoC is distributed for Research and/or Education only,
#    any commercial purpose will be FORBIDDEN.
#    PyGeoC is an open-source project,
#    but WITHOUT ANY WARRANTY; WITHOUT even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#    See the GNU General Public License for more details.
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
