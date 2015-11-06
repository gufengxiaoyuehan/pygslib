"""
pygslib: GSLIB in python

Copyright 2015, Adrian Martinez Vargas.
Licensed under MIT.
"""

import sys
from setuptools.command.test import test as TestCommand
from numpy.distutils.core import Extension

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  
        sys.exit(pytest.main(self.test_args))

""" using this convention 
 major.minor[.build[.revision]]
 with development status at third position as follow: 
    0 for alpha (status)
    1 for beta (status)
    2 for release candidate
    3 for (final) release
"""

# define properties for setup
version = '0.0.0.3.3'
description = 'Python wrap of GSLIB modified code and general geostatistical package'
name='pygslib'
long_description=open("README.rst").read()
classifiers=[ 
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Scientific/Engineering :: GIS']
keywords='geostatistics kriging variogram estimation simulation'
author='Adrian Martinez Vargas'
author_email='adriangeologo@yahoo.es'
url='https://github.com/opengeostat/pygslib'
            
if __name__ == '__main__':
     
    #fortran code extension
    #-------------------------------------------------------------------
    #make sure you use the setup from numpy
    from numpy.distutils.core import setup # this is numpy's setup
    from setuptools import find_packages
    
    # define extensions here:
    #-----------------------------------------------------  
    rotscale = Extension(name = 'pygslib.__rotscale',
                     sources = ['for_code/rotscale.f90'] )
                     
    block_covariance = Extension(name = 'pygslib.__block_covariance',
                     sources = ['for_code/block_covariance.f90'] )
                     
    read_gslib = Extension(name = 'pygslib.__read_gslib',
                     sources = ['for_code/read_gslib.f90'] )
                     
    addcoord = Extension(name = 'pygslib.__addcoord',
                     sources = ['for_code/addcoord.f90'] )                 
                     

    kt3d = Extension(name = 'pygslib.__kt3d',
                     sources = ['for_code/kt3d.f90'] )  

    plot = Extension(name = 'pygslib.__plot',
                     sources = ['for_code/plot.f90'] ) 

    declus = Extension(name = 'pygslib.__declus',
                     sources = ['for_code/declus.f90'] ) 
                     
    dist_transf = Extension(name = 'pygslib.__dist_transf',
                     sources = ['for_code/dist_transf.f90'],
                     f2py_options=[ 'only:', 'backtr', 
                                    'nscore', 'ns_ttable', ':'] ) 
    # to exclude some fortran code use this: f2py_options=['only:', 'myfoo1', 'myfoo2', ':']  
    """
    dist_transf = Extension(name = 'pygslib.__dist_transf',
                     sources = ['for_code/dist_transf.f90'],
                     f2py_options=[ '--debug-capi',
                                    'only:', 'backtr', 
                                    'nscore', 'ns_ttable', ':'] ) 
    """

    variograms = Extension(name = 'pygslib.__variograms',
                     sources = ['for_code/variograms.f90'] ) 
                     
    bigaus = Extension(name = 'pygslib.__bigaus',
                     sources = ['for_code/bigaus.f90'] ) 

    bicalib = Extension(name = 'pygslib.__bicalib',
                     sources = ['for_code/bicalib.f90'] ) 

                     
    trans = Extension(name = 'pygslib.__trans',
                     sources = ['for_code/trans.f90'] ) 
                     
    draw = Extension(name = 'pygslib.__draw',
                     sources = ['for_code/draw.f90'] ) 
    
    # define fortran code setup in here 
    setup(name=name,
          version=version,
          description= description,
          long_description=long_description,
          classifiers=classifiers,
          keywords=keywords, 
          author=author,
          author_email=author_email,
          url=url,
          license='MIT',
          packages=find_packages(exclude=['examples', 'tests']),
          include_package_data=True,
          zip_safe=False,
          tests_require=['numpy', 'pandas', 'matplotlib', 'nose', 'mock'],
          cmdclass={'test': PyTest},   
          install_requires=['numpy', 'pandas', 'matplotlib', 'nose', 'mock'],
          ext_modules = [variograms,
                         bigaus,
                         bicalib,
                         trans,
                         draw,
                         addcoord,
                         rotscale,
                         read_gslib, 
                         declus,
                         dist_transf,
                         block_covariance,
                         kt3d,
                         plot
                         ])
                         
    #cython code extension
    #-------------------------------------------------------------------
    from distutils.core import setup    # this is the standard setup
    from distutils.extension import Extension as CYExtension
    from Cython.Build import cythonize
    drillhole = CYExtension( 'pygslib.drillhole', 
                            ['cython_code/drillhole.pyx']) 
                                
    blockmodel = CYExtension( 'pygslib.blockmodel', 
                            ['cython_code/blockmodel.pyx']) 
      
    vtktools = CYExtension( 'pygslib.vtktools', 
                            ['cython_code/vtktools.pyx']) 
                            
    setup(name=name,
          version=version,
          description= description,
          long_description=long_description,
          classifiers=classifiers,
          keywords=keywords, 
          author=author,
          author_email=author_email,
          url=url,
          license='GPL',
          packages=find_packages(exclude=['examples', 'tests']),
          include_package_data=True,
          zip_safe=False,
          tests_require=['numpy', 'pandas', 'nose', 'mock'],
          cmdclass={'test': PyTest},   
          install_requires=['numpy', 'pandas', 'nose', 'mock'],
          ext_modules = [drillhole, blockmodel,vtktools])

