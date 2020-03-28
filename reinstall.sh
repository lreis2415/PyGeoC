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

# This script accepts one optional argument, i.e., the executable of python

# Set default executable of python
pythonexec=${1:-python}

cd "$PWD" || exit
rm -r dist
rm -r build
$pythonexec -m pip install tox
$pythonexec -m pip install wheel
$pythonexec setup.py bdist_wheel
cd dist || { echo "Cannot find dist directory! Reinstall PyGeoC failed!"; exit 1; }
if $pythonexec -c "import pygeoc" &> /dev/null; then
    echo 'PyGeoC has been installed, and will be uninstalled first.'
    $pythonexec -m pip install PyGeoC
else
    echo 'PyGeoC will be firstly installed.'
fi
for i in $(find . -name '*.whl'); do $pythonexec -m pip install "$i" --upgrade; done
