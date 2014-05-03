import shutil

import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ "2.1" ] = "http://downloads.sourceforge.net/winflexbison/win_flex_bison-2.1.zip"
        self.targetDigests['2.1'] = '8225e2bae867c07489cd0dc302bc529ce1a276a2'
        self.defaultTarget = "2.1"

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

        shutil.copy( os.path.join( self.imageDir(), "bin", "win_flex.exe" ) , os.path.join( self.imageDir(), "bin", "flex.exe" ) )
        shutil.copy( os.path.join( self.imageDir(), "bin", "win_bison.exe" ) , os.path.join( self.imageDir(), "bin", "bison.exe" ) )

        return True


