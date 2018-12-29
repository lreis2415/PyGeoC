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

REM This script accept one parameter, i.e., the path of python.exe

if NOT "%1" =="" (
set pypath=%1/python.exe
set pippath=%1/Scripts/pip.exe
) else (
for %%i in (python.exe) do @set pypath=%%~$PATH:i
for %%i in (pip.exe) do @set pippath=%%~$PATH:i
)
echo %pypath%
pushd %~dp0
cd %~dp0
rd /s/q dist
rd /s/q build
REM Compile and install PyGeoC through pip
%pippath% install tox
%pippath% install wheel
%pypath% setup.py bdist_wheel
cd dist
for /f "delims=" %%i in ('dir /s/b "*.whl"') do (
echo installing %%~ni ...
%pippath% install %%i --upgrade
)
cd ..