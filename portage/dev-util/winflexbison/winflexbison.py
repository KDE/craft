import shutil

import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["2.5.1" ]:
            self.targets[ ver ] = "http://downloads.sourceforge.net/winflexbison/win_flex_bison-%s.zip" % ver
        self.targetDigests['2.5.1'] = 'f7b3092bf177d0f70a6382468d837cdb217c76e8'
        self.defaultTarget = "2.5.1"

    def setDependencies( self ):
        self.buildDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.install.installPath = "bin"
