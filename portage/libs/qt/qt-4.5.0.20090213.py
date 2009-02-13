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
        self.svnTargets['4.4.3-2'] = 'branches/qt/4.4'
        self.svnTargets['svnHEAD'] = 'trunk/qt-copy/'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/dbus'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "qt-win-opensource-src-" + self.compiler
        self.openssl = "http://downloads.sourceforge.net/kde-windows/openssl-0.9.8g-1-lib.zip"
        if self.compiler == "msvc2005" or self.compiler == "msvc2008":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-msvc-1.2.4-1-lib.tar.bz2"
        elif self.compiler == "mingw":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-mingw-1.2.4-1-lib.tar.bz2"
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
        if self.buildTarget == "4.4":
          self.kdeSvnUnpack() or utils.die( "kdeSvnUnpack failed" )
        else:
          self.kdeSvnUnpack() or utils.die( "kdeSvnUnpack failed" )
          # unpack all subdirs except 'include'
          svnpath = os.path.join( self.kdesvndir, self.kdeSvnPath() )
          for subdir in "bin config.tests demos doc examples lib mkspecs patches qmake src tools translations".split():
            self.kdeSvnUnpack( self.kdeSvnPath(), subdir ) or utils.die( "kdeSvnUnpack failed" )

        svnpath = os.path.join( self.kdesvndir, self.kdeSvnPath() )

        # use our configure.exe until tt has the patches upstream
        src = os.path.join( self.packagedir, "configure.exe" )
        dst = os.path.join( svnpath, "configure.exe" )
        shutil.copyfile( src, dst )
        
        # apply patches
        os.chdir(svnpath)
        cmd = "apply_patches.py"
        self.system( cmd )

        return True

    def compile( self ):
        qtsrcdir = os.path.join( self.kdesvndir, self.kdeSvnPath() )
        qtbindir = os.path.join( self.workdir, self.instsrcdir )
        thirdparty_dir = os.path.join( self.workdir, "3rdparty" )
        configure = os.path.join( qtsrcdir, "configure.exe" ).replace( "/", "\\" )

        if not os.path.exists( qtbindir ):
          os.mkdir( qtbindir )
        os.chdir( qtbindir )

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
        os.chdir( qtbindir )
        command = r"echo y | %s -platform %s -prefix %s " \
          "-qt-gif -qt-libpng -qt-libjpeg -qt-libtiff " \
          "-no-phonon -qdbus -openssl -dbus-linked " \
          "-fast -no-vcproj -no-dsp " \
          "-nomake demos -nomake examples -nomake docs " \
          "-I \"%s\" -L \"%s\" " % \
          ( configure, platform, prefix,
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

        os.chdir( os.path.join( self.workdir, self.instsrcdir ) )
        self.system( "%s install" % self.cmakeMakeProgramm )

        src = os.path.join( self.packagedir, "qt.conf" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "qt.conf" )
        shutil.copy( src, dst )
        
        if self.buildType == "Debug" and (self.compiler == "msvc2005" or self.compiler == "msvc2008"):
            srcdir = os.path.join( self.workdir, self.instsrcdir, "lib" )
            destdir = os.path.join( self.imagedir, self.instdestdir, "lib" )

            filelist = os.listdir( srcdir )
            
            for file in filelist:
                if file.endswith( ".pdb" ):
                    shutil.copy( os.path.join( srcdir, file ), os.path.join( destdir, file ) )
                
        return True

    def make_package( self ):
        return self.doPackaging( "qt", self.buildTarget )

if __name__ == '__main__':
    subclass().execute()
