import base
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['7.6', '7.7', '7.8']:
          self.targets[ver] = 'ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'pcre-' + ver
        self.defaultTarget = '7.8'
    def setDependencies( self ):
        self.hardDependencies['dev-util/win32libs'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = False
    self.subinfo = subinfo()
    self.kdeCustomDefines += "-DBUILD_SHARED_LIBS=ON "
    self.kdeCustomDefines += "-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON "
    self.kdeCustomDefines += "-DPCRE_SUPPORT_UTF8=ON "
    self.kdeCustomDefines += "-DPCRE_EBCDIC=OFF "

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    if (not self.kdeInstall()):
      return False
    # a hack for mingw to fix my error I made in pcre 7.0
    # removeme once nobody needs pcre.dll anymore
    if self.compiler == "mingw":
        src = os.path.join( self.imagedir, self.instdestdir, "bin", "libpcre.dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "pcre.dll" )
        shutil.copy( src, dst )
        src = os.path.join( self.imagedir, self.instdestdir, "bin", "libpcrecpp.dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "mingw-pcrecpp.dll" )
        shutil.copy( src, dst )
        src = os.path.join( self.imagedir, self.instdestdir, "bin", "libpcreposix.dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "pcreposix.dll" )
        shutil.copy( src, dst )
    return True

  def make_package( self ):
    # now do packaging with kdewin-packager
    self.doPackaging( "pcre", self.buildTarget, True )
    return True
  
if __name__ == '__main__':
    subclass().execute()
