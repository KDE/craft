import base
import os
import shutil
import re
import utils
import info

PACKAGE_NAME         = "gpgme"
PACKAGE_VER          = "1.1.4"
PACKAGE_FULL_VER     = "1.1.4-3"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER)
PACKAGE_DLL_NAME     = """
libgpgme-11
"""

SRC_URI= """
ftp://ftp.gnupg.org/gcrypt/gpgme/""" + PACKAGE_FULL_NAME + """.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.1.4'] = SRC_URI
        self.svnTargets['svnHEAD'] = ""
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['dev-util/autotools'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, SRC_URI, args=args )
        self.instsrcdir = "gpgme"
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def execute( self ):
        base.baseclass.execute( self )
        if self.compiler <> "mingw":
            print "error: can only be build with MinGW (but in the end a \
                 mingw/msvc combined package is created"
            exit( 1 )

    def unpack( self ):
        if self.buildTarget == 'svnHEAD':
            repo = "svn://cvs.gnupg.org/gpgme/trunk"
            self.svndir = os.path.join( self.downloaddir, "svn-src", "gpgme" )
            self.svnFetch( repo )

            utils.cleanDirectory( self.workdir )

            # now copy the tree below destdir/trunk to workdir
            srcdir = os.path.join( self.svndir, "trunk" )
            destdir = os.path.join( self.workdir, "gpgme" )
            utils.copySrcDirToDestDir( srcdir, destdir )

            os.chdir( self.workdir )
            cmd = "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "gpgme.patch" ) )
            #self.system( cmd )
            utils.cleanDirectory( os.path.join( self.workdir, "gpgme-build" ) )
            BUILD_REVISION=0
            configure_sed = "s/BUILD_REVISION=svn_revision/BUILD_REVISION=" + repr(BUILD_REVISION) + "/g"
            os.chdir( destdir )
            cmd = "sed -i -e \"" + configure_sed + "\" configure.ac"
            self.system( cmd )
            src = os.path.join( self.workdir )
            gpgme_dir  = os.path.join( src, "gpgme" )

            cmd = "cd %s && patch -p0 < %s" % \
                  ( gpgme_dir, os.path.join( self.packagedir, "gpgme-1.1.7.diff" ) )
            self.system( cmd )
            self.msys.msysExecute( utils.toMSysPath( destdir ), "./autogen.sh", "--enable-maintainer-mode" )
            return True
        else:
            if( not base.baseclass.unpack( self ) ):
                return False
            src = os.path.join( self.workdir )
            gpgme_dir  = os.path.join( src, PACKAGE_FULL_NAME )

            cmd = "cd %s && patch -p0 < %s" % \
                  ( gpgme_dir, os.path.join( self.packagedir, "gpgme-1.1.4.diff" ) )
            self.system( cmd )

            return True

    def compile( self ):
        self.msys.instsrcdir = "gpgme"
        self.msys.msysCustomDefines = "--with-gpg-error-prefix=%s --disable-assuan" % \
                 utils.toMSysPath( self.rootdir )
        os.environ["CFLAGS"] = "-I" + utils.toMSysPath( os.path.join( self.rootdir, "include" ) )
        os.environ["LDFLAGS"] = "-L" + utils.toMSysPath( os.path.join( self.rootdir, "lib" ) )
        return self.msysCompile()

    def install( self ):
        self.instsrcdir = "gpgme"
        return self.msysInstall()

    def make_package( self ):
        # clean directory
        dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
        utils.cleanDirectory( dst )

        for lib in PACKAGE_DLL_NAME.split():
            self.stripLibs( lib )

        # auto-create both import libs with the help of pexports
        for lib in PACKAGE_DLL_NAME.split():
            self.createImportLibs( lib )

        # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
