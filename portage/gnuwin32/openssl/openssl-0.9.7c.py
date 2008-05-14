import gnuwin32
import os
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/openssl-0.9.7c-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/openssl-0.9.7c-lib.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.7c'] = SRC_URI
        self.defaultTarget = '0.9.7c'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(gnuwin32.gnuwin32class):
  def __init__( self, **args ):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()
    
  def install( self ):
    print "openssl install called"
    
    # remove this file, because it collides with the one from wget
    os.remove( os.path.join( self.workdir, "bin", "libeay32.dll" ) )
    
    gnuwin32.gnuwin32class.install( self )
    
    return True

if __name__ == '__main__':
    subclass().execute()

