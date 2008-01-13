import base
import utils
from utils import die
import os
import info

SRC_URI = """
http://heanet.dl.sourceforge.net/mingw/msysCORE-1.0.11-2007.01.19-1.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.11'] = SRC_URI
        self.defaultTarget = '1.11'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/mingw'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, SRC_URI )
        self.instdestdir = "msys"
        self.subinfo = subinfo()
	
if __name__ == '__main__':
    subclass().execute()
