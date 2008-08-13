import base
import utils
import shutil
from utils import die
import os
import info

# ok we need something more here
# dbus-lib
# openssl-lib
# we can't use kde-root/include because we get conflicting includes then
# we have to make sure that the compiler picks up the correct ones!
# --> fetch the two libs above, unpack them into a separate folder

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.4.0'] = 'ftp://ftp.trolltech.com/pub/qt/source/qt-win-opensource-src-4.4.0.zip'
        self.targets['4.4.1'] = 'ftp://ftp.trolltech.com/pub/qt/source/qt-win-opensource-src-4.4.1.zip'
        self.svnTargets['svnHEAD'] = 'trunk/qt-copy'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "qt-win-opensource-src-" + self.compiler
        self.openssl = "http://downloads.sourceforge.net/kde-windows/openssl-0.9.8g-1-lib.zip"
        if self.compiler == "msvc2005" or self.compiler == "msvc2008":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-msvc-1.2.1-2-lib.tar.bz2"
        elif self.compiler == "mingw":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-mingw-1.2.1-2-lib.tar.bz2"
        self.subinfo = subinfo()

    def fetch( self ):
        if not base.baseclass.fetch( self ):
            return False
        if not utils.getFiles( self.openssl, self.downloaddir ):
            return False
        if not utils.getFiles( self.dbuslib, self.downloaddir ):
            return False
        return True

    def unpack( self ):
        utils.cleanDirectory( self.workdir )
        # unpack our two external dependencies
        thirdparty_dir = os.path.join( self.workdir, "3rdparty" )
        files = [ os.path.basename( self.openssl ) ]
        files.append( os.path.basename( self.dbuslib ) )
        if not utils.unpackFiles( self.downloaddir, files, thirdparty_dir ):
            return False

        # and now qt
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

        # make qmake.exe create correct makefiles (moc und uic paths, reported to qt-bugs)
        cmd = "cd %s && patch -p0 < %s" % \
          ( qtsrcdir, os.path.join( self.packagedir, "qt_qmake.diff" ) )
        self.system( cmd )
        
        # patch to fix okular, sent to qt-bugs 08.06.08
        cmd = "cd %s && patch -p0 < %s" % \
          ( qtsrcdir, os.path.join( self.packagedir, "qpixmap-qimage-detach.diff" ) )
        self.system( cmd )
        
        # QtWebkit does not build if VC++ 2008 Feature Pack is installed
        if self.compiler == "msvc2008":
            cmd = "cd %s && patch -p0 < %s" % \
                ( qtsrcdir, os.path.join( self.packagedir, "msvc2008_feature_pack_xmath_fix.diff" ) )
            self.system( cmd )


        # looks like this doesn't work... hmm
        cmd = " cd %s && %s /nopause" % \
          ( os.path.join( qtsrcdir, "patches" ), "apply_patches.bat" )
        self.system( cmd )
        
        return True

    def compile( self ):
        qtsrcdir = os.path.join( self.workdir, self.instsrcdir )
        thirdparty_dir = os.path.join( self.workdir, "3rdparty" )
        os.chdir( qtsrcdir )

        # so that the mkspecs can be found, when -prefix is set
        os.putenv( "QMAKEPATH", qtsrcdir )

        # configure qt
        # prefix = os.path.join( self.rootdir, "qt" ).replace( "\\", "/" )
        prefix = os.path.join( self.imagedir, self.instdestdir )
        platform = ""
        libtmp = os.getenv( "LIB" )
        inctmp = os.getenv( "INCLUDE" )
        if self.compiler == "msvc2005":
            platform = "win32-msvc2005"
        elif self.compiler == "msvc2008":
            platform = "win32-msvc2008"
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
          "-no-phonon -qdbus -openssl -dbus-linked " \
          "-fast -no-vcproj -no-dsp " \
          "-I %s -L %s " % \
          ( platform, prefix,
            os.path.join( thirdparty_dir, "include" ),
            os.path.join( thirdparty_dir, "lib" ) )
        if self.buildType == "Debug":
          command = command + " -debug "
        else:
          command = command + " -release "
        print "command: ", command
        self.system( command )

        # build qt
        self.system( self.cmakeMakeProgramm )

        # build Qt documentation - currently does not work with mingw
        # it does not work with msvc either; unless you have a Qt4-Installation
        # already at hand. (otherwise qdoc3 fails to locate qtxml4.dll)
        #
        #if self.compiler == "msvc2005":
        #    self.system( self.cmakeMakeProgramm + " docs" )

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
        return self.doPackaging( "qt", "4.4.1-1", False )

if __name__ == '__main__':
    subclass().execute()
