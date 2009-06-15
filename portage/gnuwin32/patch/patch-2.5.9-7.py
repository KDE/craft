import base
import info
import os
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.9'] = "http://downloads.sourceforge.net/sourceforge/gnuwin32/patch-2.5.9-7-bin.zip"
        self.defaultTarget = '2.5.9'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

  def install( self ):
    base.baseclass.install( self )
    print "self.compiler: " + self.compiler
    if self.compiler == "msvc2005" or self.compiler == "msvc2008":
      manifest = os.path.join( self.packagedir, "patch.exe.manifest" )
      patch = os.path.join( self.imagedir, "bin", "patch.exe" )
      cmd = "mt.exe -nologo -manifest %s -outputresource:%s;1" % ( manifest, patch )
      utils.system( cmd )
    
    return True

if __name__ == '__main__':
    subclass().execute()
