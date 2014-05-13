import shutil

import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["2.4.2" ]:
            self.targets[ ver ] = "http://downloads.sourceforge.net/winflexbison/win_flex_bison-%s.zip" % ver
        self.targetDigests['2.4.2'] = '9e6a3a0c2ca89c1afa068aa0a055c04f5e19b722'
        self.defaultTarget = "2.4.2"

    def setDependencies( self ):
        self.buildDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.install.installPath = "bin"

    def install( self ):
        if not BinaryPackageBase.install( self ): return False
        return \
            utils.copyFile( os.path.join( self.imageDir( ), "bin", "win_flex.exe" ),
                            os.path.join( self.imageDir( ), "bin", "flex.exe" ) ) and \
            utils.copyFile( os.path.join( self.imageDir( ), "bin", "win_bison.exe" ),
                            os.path.join( self.imageDir( ), "bin", "bison.exe" ) )