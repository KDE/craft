import base
import os
import shutil
import utils
import info


class subinfo(info.infoclass):
  def setDependencies( self ):
      self.hardDependencies['dev-util/msys'] = 'default'
      self.hardDependencies['testing/glib'] = 'default'
      self.hardDependencies['testing/pkg-config'] = 'default'
	  
  def setTargets( self ):
      self.targets['0.7.2'] = 'http://kent.dl.sourceforge.net/project/gtkpod/libgpod/libgpod-0.7.2/libgpod-0.7.2.tar.gz'
      self.targetInstSrc['0.7.2'] = "libgpod-0.7.2"
      self.patchToApply['0.7.2'] = ("windows.diff", 1)
      
      self.defaultTarget = '0.7.2'

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.KDEWinPackager import *;

class Package( PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        #libxml support wont work without pkg-config libxml stuff
        self.subinfo.options.configure.defines = """--disable-libxml --disable-pygobject"""

       
    def config( self):
        os.putenv("GMSGFMT", "%s/bin/msgfmt.exe" % os.environ.get("MSYSDIR").replace('\\','/') )
        #os.putenv("LIBXML_CFLAGS","-I%s/include" % os.environ.get("KDEROOT").replace('\\','/') )
        #os.putenv("LIBXML_LIBS","-L%s/lib" % os.environ.get("KDEROOT").replace('\\','/') )
        
if __name__ == '__main__':
     Package().execute()
