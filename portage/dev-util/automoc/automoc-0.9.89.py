import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '0.9.89' ] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/automoc4.exe"
        self.defaultTarget = '0.9.89'
        ## \todo specific a target independent install path option
        self.targetInstallPath[ '0.9.89' ] = 'bin'

from Package.BinaryPackageBase import *
        
class Package( BinaryPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__( self )

    def unpack( self ):
        if not BinaryPackageBase.unpack( self ):
            return False
        if not os.path.exists( os.path.join( self.imageDir(), "lib", "automoc4" ) ):
            os.makedirs( os.path.join( self.imageDir(), "lib", "automoc4" ) )
        for filename in [ 'Automoc4Config.cmake', 'Automoc4Version.cmake', 'automoc4.files.in']:
            utils.copyFile( os.path.join( self.packageDir(), filename ), os.path.join( self.imageDir(), "lib", "automoc4", filename ) )
        return True

if __name__ == '__main__':
    Package().execute()
