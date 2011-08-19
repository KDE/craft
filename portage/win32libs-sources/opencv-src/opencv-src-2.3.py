import info
import os
from Package.CMakePackageBase import *
import compiler

if compiler.isMinGW() and os.getenv("EMERGE_USE_CCACHE") == "True":
    os.putenv("CXX","g++")
    os.putenv("CC","gcc")

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ '2.3' ]:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/opencvlibrary/OpenCV-2.3.0-win-src.zip'
            self.targetInstSrc[ ver ] = 'OpenCV-2.3.0'
        self.patchToApply['2.3'] = ('OpenCV-2.3.0-20110817.diff', 1)
        self.targetDigests['2.3'] = '126787da5a3d71e80eb6e8d3bed126391e0549c9'
        self.defaultTarget = '2.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()