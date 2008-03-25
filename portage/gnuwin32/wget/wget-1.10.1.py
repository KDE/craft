import gnuwin32
import info

SRC_URI = """
http://kent.dl.sf.net/sourceforge/gnuwin32/wget-1.10.1-bin.zip
http://kent.dl.sf.net/sourceforge/gnuwin32/wget-1.10.1-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.10.1'] = SRC_URI
        self.defaultTarget = '1.10.1'
        
class subclass(gnuwin32.gnuwin32class):
  def __init__(self):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
