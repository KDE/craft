import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '9.16' ] = "http://downloads.sourceforge.net/sourceforge/sevenzip/7za916.zip"
        self.targetDigests[ '9.16' ] = 'b389a6e2f93c18daae20393532af0e4e85ebe6f4'
        self.targetInstallPath[ '9.16' ] = "bin"
        self.defaultTarget = '9.16'
    
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True
    
    def setDependencies( self ):
        self.buildDependencies[ 'gnuwin32/wget' ]       = 'default'

from Source.SourceBase import *
from Package.PackageBase import *
from BuildSystem.BinaryBuildSystem import *

class Package( PackageBase, SourceBase, BinaryBuildSystem ):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
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
        return utils.unpackFiles( self.downloadDir(),
                [ os.path.basename( self.subinfo.target() ) ],
                os.path.join( self.imageDir(), "bin" ) )

if __name__ == '__main__':
    Package().execute()
