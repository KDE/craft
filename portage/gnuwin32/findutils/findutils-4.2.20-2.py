import gnuwin32
import info

SRC_URI = """
http://switch.dl.sourceforge.net/sourceforge/gnuwin32/findutils-4.2.20-2-dep.zip
http://switch.dl.sourceforge.net/sourceforge/gnuwin32/findutils-4.2.20-2-bin.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.2.20-2'] = SRC_URI
        self.defaultTarget = '4.2.20-2'
        
class subclass(gnuwin32.gnuwin32class):
  def __init__(self):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
