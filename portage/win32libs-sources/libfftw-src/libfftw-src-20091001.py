# -*- coding: utf-8 -*-
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '3.2.2' ] = 'http://www.fftw.org/fftw-3.2.2.tar.gz'
        self.targetDigests[ '3.2.2' ] = 'd43b799eedfb9408f62f9f056f5e8a645618467b'
        self.targetInstSrc[ '3.2.2' ] = "fftw-3.2.2"
        self.patchToApply[ '3.2.2' ] = [ ( 'fftw-3.2.2-20101125.diff', 1 ) ]

        self.defaultTarget = '3.2.2'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DFFTW_SINGLE=ON -DFFTW_DOUBLE=OFF -DBUILD_BENCHMARKS=OFF"
        
if __name__ == '__main__':
     Package().execute()
