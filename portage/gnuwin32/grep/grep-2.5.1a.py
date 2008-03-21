import gnuwin32
import info

SRC_URI = """
http://downloads.sf.net/sourceforge/gnuwin32/grep-2.5.1a-bin.zip
http://downloads.sf.net/sourceforge/gnuwin32/grep-2.5.1a-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.1a'] = SRC_URI
        self.defaultTarget = '2.5.1a'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(gnuwin32.gnuwin32class):
  def __init__(self):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
