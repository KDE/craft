import base
import os
import shutil
import utils
import info

PACKAGE_DLL_NAMES     = """
libaspell-15
libpspell-15
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.60.5'] = 'ftp://ftp.gnu.org/gnu/aspell/aspell-0.60.5.tar.gz'
        self.targetInstSrc['0.60.5'] = 'aspell-0.60.5'
        self.defaultTarget = '0.60.5'
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False

    src = os.path.join( self.workdir, self.instsrcdir )
    cmd = "cd %s && patch -p0 < %s" % \
          ( src, os.path.join( self.packagedir , "aspell-0.60.5.diff" ) )
    utils.system( cmd )
    return True

  def compile( self ):
    return self.msysCompile( False )

  def install( self ):
    return self.msysInstall( False )

  def make_package( self ):
    for libs in PACKAGE_DLL_NAMES.split():
        self.stripLibs( libs )

    # auto-create both import libs with the help of pexports
    # one problem here - aspell has also a c++ interface which can't be used...
    # -> remove those functions from the export libs
    for libs in PACKAGE_DLL_NAMES.split():
        self.createImportLibs( libs )

    # now do packaging with kdewin-packager
    self.doPackaging( "aspell", self.buildTarget, False )

    return True

if __name__ == '__main__':
    subclass().execute()
