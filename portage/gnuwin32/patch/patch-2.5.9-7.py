import os
import info
import utils
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.9'] = "http://downloads.sourceforge.net/sourceforge/gnuwin32/patch-2.5.9-7-bin.zip"
        self.targetDigests['2.5.9'] = '7b2ec738881f4e962e54e0f330b67c42635266b7'
        self.defaultTarget = '2.5.9'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        if compiler.isMinGW():
            self.hardDependencies['dev-util/uactools'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True
    
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

    def install( self ):
        if not BinaryBuildSystem.install( self ):
            return False
        manifest = os.path.join( self.packageDir(), "patch.exe.manifest" )
        patch = os.path.join( self.installDir(), "bin", "patch.exe" )
        cmd = "mt.exe -nologo -manifest %s -outputresource:%s;1" % ( manifest, patch )
        utils.system( cmd )

        return True
        
if __name__ == '__main__':
    Package().execute()
