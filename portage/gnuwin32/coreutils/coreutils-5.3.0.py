import gnuwin32
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/coreutils-5.3.0-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/coreutils-5.3.0-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.3.0'] = SRC_URI
        self.defaultTarget = '5.3.0'
        
class subclass(gnuwin32.gnuwin32class):
  def __init__( self, **args ):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
