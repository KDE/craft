import base
import os
import utils
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.4.2-3'] = "http://fontconfig.org/release/fontconfig-2.4.2.tar.gz"
        self.targetInstSrc['2.4.2-3'] = PACKAGE_FULL_NAME
        self.defaultTarget = '2.4.2-3'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin32'] = 'default'
        self.hardDependencies['win32libs-sources/freetype-src'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = False
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir, "fontconfig-cmake.diff" ) )
        self.system( cmd ) or utils.die( "patch" )

        return True

    def kdeSvnPath( self ):
        return False
    
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        self.doPackaging( "fontconfig", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
