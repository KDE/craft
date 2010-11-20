import base
import os
import shutil
import re
import utils
import info

#
# this library is used by kdeedu/kstars
# the library is c-only but it may not work due to __stdcall - we'll see
# it should be no problem to compile it with msvc and/or create a CMakeLists.txt
# to fix this problem if there's one
#

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.08'] = 'ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio3080.tar.gz'
        self.targets['3.10'] = 'ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio3100.tar.gz'
        self.targets['3.14'] = 'ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio3140.tar.gz'
        self.targets['3.20'] = 'ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio3200.tar.gz'
        self.targetInstSrc['3.08'] = "cfitsio"
        self.targetInstSrc['3.10'] = "cfitsio"
        self.targetInstSrc['3.14'] = "cfitsio"
        self.targetInstSrc['3.20'] = "cfitsio"
        self.defaultTarget = '3.20'

    def setDependencies( self ):
        self.buildDependencies['virtual/base']  = 'default'
        self.buildDependencies['dev-util/msys'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, "", args=args )
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def execute( self ):
        base.baseclass.execute( self )
        if not self.compiler.startswith( "mingw" ):
            print "error: can only be build with MinGW right now."
            exit( 1 )

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
            
        src = os.path.join( self.workdir, self.instsrcdir )

        cmd = "cd %s && patch -p0 < %s" % \
              ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir , "configure.diff" ) )
        if utils.verbose() >= 1:
            print cmd
        self.system( cmd )

        cmd = "cd %s && patch -p0 < %s" % \
              ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir , "Makefile.in.diff" ) )
        if utils.verbose() >= 1:
            print cmd
        self.system( cmd )
        
        return True

    def msysConfigureFlags ( self ):
        flags = "--prefix=/ "
        return flags

    def compile( self ):
        return self.msysCompile( False )

    def install( self ):
        return self.msysInstall( False )

    def make_package( self ):
        dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
        utils.cleanDirectory( dst )

        self.stripLibs( "libcfitsio" )
        self.createImportLibs( "libcfitsio" )
        # now do packaging with kdewin-packager
        # it's a in-source build, do not pack sources
        self.doPackaging( "cfitsio", self.buildTarget, False )

        return True

if __name__ == '__main__':
    subclass().execute()
