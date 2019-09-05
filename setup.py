import sys, os, platform, glob
from distutils.core import setup
from setuptools import *

"""
Setup script for FusionVet  -- A bioinformatics tool to visualize and evaluate *known* gene fusions.
"""

def main():
    setup(  name = "FusionVet",
            version = "1.0.0",
            python_requires='>=3.5',
            py_modules = [ 'psyco_full' ],
            packages = find_packages( 'lib' ),
            package_dir = { '': 'lib' },
            package_data = { '': ['*.ps'] },
            scripts = glob.glob( "bin/*.py"),
            ext_modules = [],
            test_suite = 'nose.collector',
            setup_requires = ['nose>=0.10.4'],
            author = "Liguo Wang",
            author_email ="wangliguo78@gmail.com",
            platforms = ['Linux','MacOS'],
            requires = [],
            install_requires = ['numpy','scipy','pysam'], 
            description = "A bioinformatics tool to visualize and evaluate *known* gene fusions",
            url = "https://fusionvet.readthedocs.io/en/latest/index.html",
            zip_safe = False,
            dependency_links = [],
            classifiers=[
                'Development Status :: 5 - Production/Stable',
                'Environment :: Console',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                'Operating System :: MacOS :: MacOS X',
                'Operating System :: POSIX',
                'Programming Language :: Python',
                'Topic :: Scientific/Engineering :: Bio-Informatics',
            ],
            
            keywords='gene fusion, validation, visualization, UCSC, BAM, bed, bigBed, interact, bigInteract',
             )


if __name__ == "__main__":
    main()
