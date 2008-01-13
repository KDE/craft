import base
import os
import shutil
import info

SRC_URI = "http://homepages.compuserve.de/SiegwardJaekel/mc.zip"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.1.36'] = SRC_URI
        self.defaultTarget = '4.1.36'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.instdestdir = "mc"
    self.subinfo = subinfo()

  def compile( self ):
    print "mc compile called"
    f = open( os.path.join( self.workdir, "mcedit.bat" ), "wb" )
    f.write( "mc -e %1" )
    f.close()
    # mc is also a program in visual studio,
    # so make the real mc reachable from mcc too...
    shutil.copy( os.path.join( self.workdir, "mc.exe" ), 
	os.path.join( self.workdir, "mcc.exe" ) )
    return True
    
if __name__ == '__main__':
    subclass().execute()
