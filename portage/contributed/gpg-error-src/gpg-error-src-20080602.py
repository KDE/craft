import base
import os
import shutil
import re
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.5'] = """ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-1.5.tar.bz2"""
        self.targetInstSrc['1.5'] = 'libgpg-error-1.5'
        self.targets['1.6'] = """ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-1.6.tar.bz2"""
        self.targetInstSrc['1.6'] = 'libgpg-error-1.6'
        self.defaultTarget = '1.6'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, "", args=args )
        self.instsrcdir = "gpgerr"
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def execute( self ):
        base.baseclass.execute( self )
        if self.compiler <> "mingw":
            print "error: can only be build with MinGW (but in the end a \
                 mingw/msvc combined package is created"
            exit( 1 )

    def unpack( self ):
        if self.buildTarget == '1.6':
            if( not base.baseclass.unpack( self ) ):
                return False
            src = os.path.join( self.workdir )
            gpgerr_dir = os.path.join( src, "libgpg-error-1.6" )

            cmd = "cd %s && patch -p0 < %s" % \
                  ( gpgerr_dir, os.path.join( self.packagedir, "libgpg-error-1.6.diff" ) )
            self.system( cmd )
            return True
        else:
            if( not base.baseclass.unpack( self ) ):
                return False
            src = os.path.join( self.workdir )
            gpgerr_dir = os.path.join( src, "libgpg-error-1.5" )

            cmd = "cd %s && patch -p0 < %s" % \
                  ( gpgerr_dir, os.path.join( self.packagedir, "libgpg-error-1.5.diff" ) )
            self.system( cmd )
            return True

    def compile( self ):
        return self.msysCompile()

    def install( self ):
        return self.msysInstall()

    def make_package( self ):
        # clean directory
        dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
        utils.cleanDirectory( dst )

        PACKAGE_DLL_NAME="""libgpg-error-0"""
        for lib in PACKAGE_DLL_NAME.split():
            self.stripLibs( lib )

        # auto-create both import libs with the help of pexports
        for lib in PACKAGE_DLL_NAME.split():
            self.createImportLibs( lib )

        # now do packaging with kdewin-packager
        self.doPackaging( "libgpg-error", "libgpg-error-" + self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
