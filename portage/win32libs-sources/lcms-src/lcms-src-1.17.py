import base
import os
import shutil
import re
import utils
import info

PACKAGE_NAME         = "lcms"
PACKAGE_VER          = "1.17"
PACKAGE_FULL_VER     = "1.17"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = """
liblcms-1
"""

SRC_URI= """
http://www.littlecms.com/lcms-1.17.tar.gz
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['1.17'] = SRC_URI
        self.defaultTarget = '1.17'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/win32libs'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.instsrcdir = PACKAGE_FULL_NAME
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def execute( self ):
    base.baseclass.execute( self )
    if self.compiler <> "mingw":
      print "error: can only be build with MinGW (but in the end a \
             mingw/msvc combined package is created"
      exit( 1 )

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False;
    # the .tar.gz ships a wrong icc34.h - it must be generated from icc34.h.in
    file = os.path.join( self.workdir, self.instsrcdir, "include", "icc34.h" )
    if( os.path.isfile( file ) ):
      os.remove( file )
    return True

  def compile( self ):
    libpath = os.path.join( self.rootdir, "win32libs", "lib" )
    incpath = os.path.join( self.rootdir, "win32libs", "include" )
    print libpath
    print incpath
    os.environ[ "LDFLAGS" ] = "-L" + utils.toMSysPath( libpath )
    os.environ[ "CFLAGS" ]  = "-I" + utils.toMSysPath( incpath )
    return self.msysCompile()

  def install( self ):
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
