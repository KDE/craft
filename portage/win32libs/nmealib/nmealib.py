import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0.5.3']:
            self.targets[ver] = ' http://freefr.dl.sourceforge.net/project/nmea/NmeaLib/nmea-0.5.x/nmealib-%s.zip' % ver
            self.targetInstSrc[ver] = 'nmealib'
        self.patchToApply[ '0.5.3' ] = [
            ( "0001-Make-the-library-compile-on-C99-compilers.patch", 1 ),
            ( "0002-Generate-position-independent-code-PIC.patch", 1 ),
            ( "0003-Allow-the-parser-to-be-destroyed-when-its-buffer-is-.patch", 1 ),
            ( "0004-Print-the-results-in-the-parsing-sample-program.patch", 1 ),
            ( "0005-Optimise-generated-code-and-show-all-warnings-during.patch", 1 ),
            ( "0006-Fix-a-warning.patch", 1 ),
            ( "0007-Add-install-target.patch", 1 ),
            ( "0008-cmake-support.patch", 1 ),
            ( "0009-feet-unit-elevation-fix.patch", 1 ),
            ( "0010-lc_numeric-locale-win32-fix.patch", 1)
        ]
        self.targetDigests['0.5.3'] = '54a30c4791fd27a8e631728219ace8729d6d92f9'
        self.shortDescription = "library for handling NMEA protocol"
        self.defaultTarget = '0.5.3'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
