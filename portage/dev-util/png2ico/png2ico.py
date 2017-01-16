import shutil

import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ "2002-12-08" ] = "http://www.winterdrache.de/freeware/png2ico/data/png2ico-win-2002-12-08.zip"
        self.targetDigests['2002-12-08'] = 'c3b5fbe0e5c1cb290f7d77dc124922a0ddb8e9d2'
        self.defaultTarget = "2002-12-08"

    def setDependencies( self ):
        self.buildDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.destinationPath = "dev-utils"
        
    def install( self ):
        if not BinaryPackageBase.install(self):
            return False
        os.mkdir(os.path.join( self.imageDir( ), "bin"))
        utils.moveFile( os.path.join( self.imageDir( ), "png2ico", "png2ico.exe" ),
                       os.path.join( self.imageDir( ), "bin", "png2ico.exe" ) )
        utils.rmtree( os.path.join( self.imageDir( ), "png2ico" ))
        return True