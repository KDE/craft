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

#DEPEND = """
#dev-util/win32libs
#virtual/base
#"""

SRC_URI= """
ftp://ftp.tu-chemnitz.de/pub/Qt/qt/source/""" + PACKAGE_FULL_NAME + """.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.3.3-2'] = SRC_URI
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

    def unpack( self ):
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
            self.system( cmd ) and utils.die( "qt unpack failed" )

            # disable debug build of qdbus tools to avoid linking problems (reported on kde-windows)
            cmd = "cd %s && patch -p0 < %s" % \
              ( qtsrcdir, os.path.join( self.packagedir, "qdbus.diff" ) )
            self.system( cmd ) and utils.die( "qt unpack failed" )

            # install qtestlib into /bin
            cmd = "cd %s && patch -p0 < %s" % \
              ( qtsrcdir, os.path.join( self.packagedir, "qtestlib.diff" ) )
            self.system( cmd ) and utils.die( "qt unpack failed" )
        else:
            qtsrcdir = os.path.join( self.workdir, self.instsrcdir )
            
            utils.cleanDirectory( qtsrcdir )
            self.kdeSvnUnpack() or utils.die( "kdeSvnUnpack failed" )
            
            if self.noCopy:
                srcdir = os.path.join(self.kdesvndir, self.kdeSvnPath() ).replace("/", "\\")
                utils.copySrcDirToDestDir( srcdir, qtsrcdir )

            # disable demos and examples
            sedcommand = r""" -e "s:SUBDIRS += examples::" -e "s:SUBDIRS += demos::" """
            utils.sedFile( qtsrcdir, "projects.pro", sedcommand )

            # patch to disable building of pbuilder_pbx.cpp, as it takes ages
            path = os.path.join( qtsrcdir, "qmake" )
            file = "Makefile.win32-g++"
            sedcommand = """ -e "s/pbuilder_pbx.o//" """
#            utils.sedFile( path, file, sedcommand )
            
        return True

    def compile( self ):
        qtsrcdir = os.path.join( self.workdir, self.instsrcdir )
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
        if self.traditional:
            win32incdir = os.path.join( self.rootdir, "win32libs", "include" ).replace( "\\", "/" )
            win32libdir = os.path.join( self.rootdir, "win32libs", "lib" ).replace( "\\", "/" )
        else:
            win32incdir = os.path.join( self.rootdir, "include" ).replace( "\\", "/" )
            win32libdir = os.path.join( self.rootdir, "lib" ).replace( "\\", "/" )

        # recommended from README.qt-copy
        #  "configure.exe -prefix ..\..\image\qt -platform win32-g++ " \
        #  "-qt-gif -no-exceptions -debug -system-zlib -system-libpng -system-libmng " \
        #  "-system-libtiff -system-libjpeg -openssl " \
        #  "-I %s -L %s" % ( win32incdir, win32libdir )

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
          "-qdbus -qt-gif -no-exceptions -qt-libpng " \
          "-system-libjpeg -system-libtiff -openssl " \
          "-fast -no-vcproj -no-dsp -no-style-windowsvista " \
          "-I %s -L %s " % \
          ( platform, prefix, win32incdir, win32libdir )
        print "command: ", command
        self.system( command ) or utils.die( "qt configure failed" )

        # build qt
        self.system( self.cmakeMakeProgramm ) or utils.die( "qt make failed" )

        if( not libtmp == None ):
            os.environ[ "LIB" ] = libtmp
        if( not inctmp == None ):
            os.environ[ "INCLUDE" ] = inctmp
        return True

    def install( self ):
        qtsrcdir = os.path.join( self.workdir, self.instsrcdir )
        os.chdir( qtsrcdir )

        self.system( "%s install" % self.cmakeMakeProgramm ) or utils.die( "qt make install failed" )

        src = os.path.join( self.packagedir, "qt.conf" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "qt.conf" )
        shutil.copy( src, dst )

        return True

    def make_package( self ):
        return self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

if __name__ == '__main__':
    subclass().execute()
