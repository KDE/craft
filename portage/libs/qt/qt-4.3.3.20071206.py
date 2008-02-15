import base
import utils
import shutil
from utils import die
import os
import info

PACKAGE_NAME         = "qt"
PACKAGE_VER          = "4.3.3"
PACKAGE_FULL_VER     = "4.3.3-2"
PACKAGE_FULL_NAME    = "%s-win-opensource-src-%s" % ( PACKAGE_NAME, PACKAGE_VER )

# ok we need something more here
# dbus-lib
# openssl-lib
# we can't use kde-root/include because we get conflicting includes then
# we have to make sure that the compiler picks up the correct ones!
# --> fetch the two libs above, unpack them into a separate folder

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.3.3-2'] = 'ftp://ftp.tu-chemnitz.de/pub/Qt/qt/source/' + PACKAGE_FULL_NAME + '.zip'
        self.targetInstSrc['4.3.3-2'] = "qt-win-opensource-src-4.3.3" + "-" + os.getenv( "KDECOMPILER" )
        self.svnTargets['qt-copy'] = 'trunk/qt-copy'
        self.defaultTarget = '4.3.3-2'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "qt-win-opensource-src-" + self.compiler
        self.subinfo = subinfo()

    def fetch( self ):
        if not base.baseclass.fetch( self ):
            return False
        openssl = "http://82.149.170.66/kde-windows/repository/win32libs/single/openssl-0.9.8g-1-lib.zip"
        if self.compiler == "msvc2005":
            dbuslib = "http://download.cegit.de/kde-windows/repository/win32libs/single/dbus-msvc-1.1.2.20071228-bin.tar.bz2"
        elif self.compiler == "mingw":
            dbuslib = "http://download.cegit.de/kde-windows/repository/win32libs/single/dbus-mingw-1.1.2.20071228-lib.tar.bz2"

        if not utils.getFiles( openssl, self.downloaddir ):
            return False
        if not utils.getFiles( dbuslib, self.downloaddir ):
            return False
        return True

    def unpack( self ):
        utils.cleanDirectory( self.workdir )
        # unpack our two external dependencies
        thirdparty_dir = os.path.join( self.workdir, "3rdparty" )
        files = "openssl-0.9.8g-1-lib.zip "
        if self.compiler == "msvc2005":
            files += "dbus-msvc-1.1.2.20071228-lib.tar.bz2"
        elif self.compiler == "mingw":
            files += "dbus-mingw-1.1.2.20071228-lib.tar.bz2"
        if not utils.unpackFiles( self.downloaddir, files.split(), thirdparty_dir ):
            return False

        # and now qt
        if self.buildTarget == '4.3.3-2':
            qtsrcdir = os.path.join( self.workdir, self.instsrcdir )
            qtsrcdir_tmp = os.path.join( self.workdir, PACKAGE_FULL_NAME )

            utils.cleanDirectory( qtsrcdir )
            utils.cleanDirectory( qtsrcdir_tmp )

            if ( not utils.unpackFile( self.downloaddir, self.filenames[0], self.workdir ) ):
                return False
            os.rmdir( qtsrcdir )
            os.rename( qtsrcdir_tmp, qtsrcdir )

            # disable demos and examples
            sedcommand = r""" -e "s:SUBDIRS += examples::" -e "s:SUBDIRS += demos::" """
            utils.sedFile( qtsrcdir, "projects.pro", sedcommand )

            # patch to disable building of pbuilder_pbx.cpp, as it takes ages
            path = os.path.join( qtsrcdir, "qmake" )
            file = "Makefile.win32-g++"
            sedcommand = """ -e "s/pbuilder_pbx.o//" """
            utils.sedFile( path, file, sedcommand )

            # disable usage of it
            path = os.path.join( qtsrcdir, "qmake", "generators" )
            file = "metamakefile.cpp"
            sedcommand = r""" -e "s:^.*ProjectBuilder://\0:" """
            utils.sedFile( path, file, sedcommand )

            # help qt a little bit :)
            cmd = "cd %s && patch -p0 < %s" % \
              ( qtsrcdir, os.path.join( self.packagedir, "qt-4.3.3.diff" ) )
            self.system( cmd )

            # disable debug build of qdbus tools to avoid linking problems (reported on kde-windows)
            cmd = "cd %s && patch -p0 < %s" % \
              ( qtsrcdir, os.path.join( self.packagedir, "qdbus.diff" ) )
            self.system( cmd )

            # install qtestlib into /bin
            cmd = "cd %s && patch -p0 < %s" % \
              ( qtsrcdir, os.path.join( self.packagedir, "qtestlib.diff" ) )
            self.system( cmd )
        else:
            qtsrcdir = os.path.join( self.workdir, self.instsrcdir )
            
            utils.cleanDirectory( qtsrcdir )
            self.kdeSvnUnpack() or utils.die( "kdeSvnUnpack failed" )

            # noCopy isn't possible for qt
            if self.noCopy:
                srcdir = os.path.join(self.kdesvndir, self.kdeSvnPath() )
                utils.copySrcDirToDestDir( srcdir, qtsrcdir )

            # disable demos and examples
            sedcommand = r""" -e "s:SUBDIRS += examples::" -e "s:SUBDIRS += demos::" """
            utils.sedFile( qtsrcdir, "projects.pro", sedcommand )

            # disable debug build of qdbus tools to avoid linking problems (reported on kde-windows)
            cmd = "cd %s && patch -p0 < %s" % \
              ( qtsrcdir, os.path.join( self.packagedir, "qdbus-qt4.4.diff" ) )
            self.system( cmd )

        return True

    def compile( self ):
        qtsrcdir = os.path.join( self.workdir, self.instsrcdir )
        thirdparty_dir = os.path.join( self.workdir, "3rdparty" )
        os.chdir( qtsrcdir )

        # so that the mkspecs can be found, when -prefix is set
        os.putenv( "QMAKEPATH", qtsrcdir )

        if self.buildTarget == '4.3.3-2':
            utils.warning( "************************************************************************************\n" \
                           "This Target might be deprecated and is going to be replaced with the target qt-copy.\n" \
                           "Since qt-copy might not have best stability, you might choose to install this target\n" \
                           "though. If you're not sure what to do, kill the current process with Ctrl+C and ask\n" \
                           "on irc or on the mailing list."\
                           "************************************************************************************\n" )

        # configure qt
        # prefix = os.path.join( self.rootdir, "qt" ).replace( "\\", "/" )
        prefix = os.path.join( self.imagedir, self.instdestdir )
        platform = ""
        libtmp = os.getenv( "LIB" )
        inctmp = os.getenv( "INCLUDE" )
        if self.compiler == "msvc2005":
            platform = "win32-msvc2005"
        elif self.compiler == "mingw":
            os.environ[ "LIB" ] = ""
            os.environ[ "INCLUDE" ] = ""
            platform = "win32-g++"
        else:
            exit( 1 )

        os.environ[ "USERIN" ] = "y"
        os.chdir( qtsrcdir )
        command = r"echo y | configure.exe -platform %s -prefix %s " \
          "-qt-gif -qt-libpng -qt-libjpeg -qt-libtiff " \
          "-qdbus -openssl " \
          "-fast -no-vcproj -no-dsp " \
          "-I %s -L %s " % \
          ( platform, prefix,
            os.path.join( thirdparty_dir, "include" ),
            os.path.join( thirdparty_dir, "lib" ) )
        print "command: ", command
        self.system( command )

        # build qt
        self.system( self.cmakeMakeProgramm )

        if( not libtmp == None ):
            os.environ[ "LIB" ] = libtmp
        if( not inctmp == None ):
            os.environ[ "INCLUDE" ] = inctmp
        return True

    def install( self ):
        qtsrcdir = os.path.join( self.workdir, self.instsrcdir )
        os.chdir( qtsrcdir )

        self.system( "%s install" % self.cmakeMakeProgramm )

        src = os.path.join( self.packagedir, "qt.conf" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "qt.conf" )
        shutil.copy( src, dst )

        return True

    def make_package( self ):
        return self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

if __name__ == '__main__':
    subclass().execute()
