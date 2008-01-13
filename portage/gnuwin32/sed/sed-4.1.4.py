import gnuwin32
import info

SRC_URI = """
http://switch.dl.sf.net/sourceforge/gnuwin32/sed-4.1.4-bin.zip
http://switch.dl.sf.net/sourceforge/gnuwin32/sed-4.1.4-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.1.4'] = SRC_URI
        self.defaultTarget = '4.1.4'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
class subclass(gnuwin32.gnuwin32class):
    def __init__(self):
        gnuwin32.gnuwin32class.__init__( self, SRC_URI )
        self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
