import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/sed-4.1.5-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/sed-4.1.5-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.1.5'] = SRC_URI
        self.defaultTarget = '4.1.5'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
