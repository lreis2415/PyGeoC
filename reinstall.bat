REM
REM    This file is aimed for reCompile and reInstall PyGeoC for debugging on Windows platform.
REM
REM    PyGeoC is distributed for Research and/or Education only,
REM    any commercial purpose will be FORBIDDEN.
REM    PyGeoC is an open-source project,
REM    but WITHOUT ANY WARRANTY; WITHOUT even the implied warranty of
REM    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
REM
REM    See the GNU General Public License for more details.
REM

pushd %~dp0
cd %~dp0
rd /s/q dist
rd /s/q build
REM Compile and install PyGeoC through pip
pip install tox
pip install wheel
python setup.py bdist_wheel
cd dist
for /f "delims=" %%i in ('dir /s/b "*.whl"') do (
echo installing %%~ni ...
pip install %%i --upgrade
)