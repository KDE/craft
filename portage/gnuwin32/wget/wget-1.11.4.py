import gnuwin32
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/wget-%s-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/wget-%s-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        for t in ( '1.10.1', '1.11.4' ):
          self.targets[ t ] = SRC_URI % ( t, t )
        self.defaultTarget = '1.11.4'
        
class subclass(gnuwin32.gnuwin32class):
  def __init__( self, **args ):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
