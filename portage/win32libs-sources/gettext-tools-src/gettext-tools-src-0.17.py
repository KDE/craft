import base
import os
import shutil
import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
      self.targets['0.17'] = 'http://ftp.gnome.org/pub/gnome/binaries/win32/dependencies/gettext-tools-0.17.zip'
      self.targetInstSrc['0.17'] = ''
      self.defaultTarget = '0.17'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    # that's one of the best packages I've seen from gnuwin32 - nothing to do here :)
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir, self.instsrcdir )
    utils.copySrcDirToDestDir( src, dst )

    return True

  def make_package( self ):
    self.instsrcdir = ""

    # now do packaging with kdewin-packager
    self.doPackaging( "gettext-tools", self.buildTarget, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
