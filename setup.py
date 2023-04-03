"""A setuptools based setup module for PyGeoC.
   PyGeoC is short for "Python for GeoComputation"
   Author: Liangjun Zhu
   E-mail: zlj@lreis.ac.cn
   Blog  : zhulj.net
"""

# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import setup
from setuptools.command.test import test as TestCommand

import pygeoc

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# class Tox(TestCommand):
#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True
#
#     def run_tests(self):
#         # import here, cause outside the eggs aren't loaded
#         import tox, sys
#         errcode = tox.cmdline(self.test_args)
#         sys.exit(errcode)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        import sys
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
        name='PyGeoC',

        # Versions should comply with PEP440.  For a discussion on single-sourcing
        # the version across setup.py and the project code, see
        # https://packaging.python.org/en/latest/single_source_version.html
        version=pygeoc.__version__,

        description='Python for GeoComputation',
        long_description='Using Python to handle GeoComputation such as hydrologic analysis'
                         'by gridded DEM.',

        # The project's main homepage.
        url=pygeoc.__url__,

        # Author details
        author=pygeoc.__author__,
        author_email=pygeoc.__email__,

        # Choose your license
        license='MIT',

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            # How mature is this project? Common values are
            #   1 - Planning
            #   2 - Pre-Alpha
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: GIS',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
        ],

        # What does your project relate to?
        keywords='GeoComputation utility library',

        # You can just specify the packages manually here if your project is
        # simple. Or you can use find_packages().
        packages=['pygeoc'],

        # Alternatively, if you want to distribute just a my_module.py, uncomment
        # this:
        #   py_modules=["my_module"],

        # List run-time dependencies here.  These will be installed by pip when
        # your project is installed. For an analysis of "install_requires" vs pip's
        # requirements files see:
        # https://packaging.python.org/en/latest/requirements.html
        install_requires=[
            # In case of incompatibility, users are encouraged to
            #   install these required package by themselves.
            # See requirements.txt and requirements_dev.txt for more details.
            # 'gdal>=1.9.0',
            # 'numpy>=1.9.0',
            # 'matplotlib',
            'typing;python_version<"3.5"',
            'future',
            'six',
            'configparser;python_version<"3"'
        ],

        # List additional groups of dependencies here (e.g. development
        # dependencies). You can install these using the following syntax,
        # for example:
        # $ pip install -e .[dev,test]
        extras_require={'testing': ['pytest']},

        # If there are data files included in your packages that need to be
        # installed, specify them here.  If using Python 2.6 or less, then these
        # have to be included in MANIFEST.in as well.
        package_data={},

        # Although 'package_data' is the preferred approach, in some case you may
        # need to place data files outside of your packages. See:
        # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
        # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
        # data_files=[('my_data', ['data/data_file'])],
        data_files=[],
        tests_require=['pytest'],
        # cmdclass={'test': Tox},
        cmdclass={'test': PyTest},
        # To provide executable scripts, use entry points in preference to the
        # "scripts" keyword. Entry points provide cross-platform support and allow
        # pip to create the appropriate form of executable for the target platform.
        entry_points={
            'console_scripts': [
                'PyGeoC=PyGeoC:main',
            ],
        },
)
