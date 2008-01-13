import base
import os
import utils
import info

PACKAGE_NAME         = "poppler"
PACKAGE_VER          = "0.6.3"
PACKAGE_FULL_VER     = "0.6.3"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "poppler"

SRC_URI = """
http://poppler.freedesktop.org/poppler-0.6.3.tar.gz
http://poppler.freedesktop.org/poppler-data-0.2.0.tar.gz
"""

##http://poppler.freedesktop.org/""" + PACKAGE_FULL_NAME + """.tar.gz
##"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['0.6.3'] = SRC_URI
        self.defaultTarget = '0.6.3'
    
    def setDependencies( self ):
        self.hardDependencies['testing/fontconfig-src'] = 'default'
        self.hardDependencies['testing/freetype-src'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, SRC_URI )
        self.instsrcdir = PACKAGE_FULL_NAME
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
            
        src = os.path.join( self.workdir, self.instsrcdir )

        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir , "poppler-cmake.patch" ) )
        if utils.verbose() >= 1:
            print cmd
        self.system( cmd ) or die( "patch" )
        return True
        
        
    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_QT4_TESTS=ON"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def kdeSvnPath( self ):
        return False
        
    def make_package( self ):
        # auto-create both import libs with the help of pexports
        #self.stripLibs( PACKAGE_DLL_NAME )

        # auto-create both import libs with the help of pexports
        #self.createImportLibs( PACKAGE_DLL_NAME )

        # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
