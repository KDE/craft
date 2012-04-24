import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0.5.3']:
            self.targets[ver] = ' http://freefr.dl.sourceforge.net/project/nmea/NmeaLib/nmea-0.5.x/nmealib-%s.zip' % ver
            self.targetInstSrc[ver] = 'nmealib'
        self.patchToApply[ '0.5.3' ] = [ ( "nmealib-20120424.diff", 1 ) ]
        self.targetDigests['0.5.3'] = '54a30c4791fd27a8e631728219ace8729d6d92f9'
        self.shortDescription = "library for handling NMEA protocol"
        self.defaultTarget = '0.5.3'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
