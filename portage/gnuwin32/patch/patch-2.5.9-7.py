import gnuwin32
import info
import os
import shutil

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/patch-2.5.9-7-bin.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.9'] = SRC_URI
        self.defaultTarget = '2.5.9'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(gnuwin32.gnuwin32class):
  def __init__( self, **args ):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()

  def install( self ):
    gnuwin32.gnuwin32class.install( self )

    manifest = os.path.join( self.packagedir , "patch.exe.manifest" )
    if self.traditional:
        manifest_dest = os.path.join( self.imagedir, "gnuwin32", "bin" )
    else:
        manifest_dest = os.path.join( self.imagedir, "bin" )

    shutil.copy( manifest, manifest_dest )
    return True

if __name__ == '__main__':
    subclass().execute()
