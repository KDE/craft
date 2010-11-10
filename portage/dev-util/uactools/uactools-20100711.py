# uactools : Binary package of the tools to handle UAC from kde-windows.
# mt.exe can be used to embed manifest files to disable heuristic UAC raise
# requests, setuac.exe can be used to enable raise the privileges of a program.
# The according source package is uactools-pkg

import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        latest = "20100711"
        self.targets[ latest ] = \
            "http://downloads.sourceforge.net/project/kde-windows/uactools/uactools-mingw4-" + \
            latest + "-bin.tar.bz2"
        self.targetDigests[ latest ] = 'b59ab7ac9190cbfe5b00acae05f909ea8f22bd3a'
        self.defaultTarget = latest

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

from Source.SourceBase import *
from Package.PackageBase import *
from BuildSystem.BinaryBuildSystem import *

class Package( PackageBase, SourceBase, BinaryBuildSystem ):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.install.installPath = "bin"
        SourceBase.__init__( self )
        PackageBase.__init__( self )
        BinaryBuildSystem.__init__( self )
        
    def fetch( self ):
        filenames = [ os.path.basename( self.subinfo.target() ) ]

        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True

        self.setProxy()
        return utils.getFiles( self.subinfo.target(), self.downloadDir() )

    def unpack( self ):
        return utils.unpackFiles( self.downloadDir(), [ os.path.basename( self.subinfo.target() ) ], self.imageDir() )

if __name__ == '__main__':
    Package().execute() 
