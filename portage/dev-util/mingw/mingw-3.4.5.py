import base
import utils
from utils import die
import os
import info

"""
from trolltech mingw package:

binutils-2.15.91-20040904-1.tar.gz
gcc-core-3.4.2-20040916-1.tar.gz
gcc-g++-3.4.2-20040916-1.tar.gz
mingw32-make-3.80.0-3.exe
mingw-runtime-3.7.tar.gz -> 3.9
w32api-3.2.tar.gz -> 3.6
"""

SRC_URI = """
http://heanet.dl.sourceforge.net/sourceforge/mingw/binutils-2.18.50-20080109.tar.gz
http://heanet.dl.sourceforge.net/sourceforge/mingw/gcc-core-3.4.5-20060117-1.tar.gz
http://heanet.dl.sourceforge.net/sourceforge/mingw/gcc-g++-3.4.5-20060117-1.tar.gz
http://heanet.dl.sourceforge.net/sourceforge/mingw/mingw32-make-3.81-2.tar.gz
http://heanet.dl.sourceforge.net/sourceforge/mingw/mingw-runtime-3.13.tar.gz
http://heanet.dl.sourceforge.net/sourceforge/mingw/w32api-3.11.tar.gz
http://heanet.dl.sourceforge.net/sourceforge/mingw/gdb-6.7.50.20071127-mingw.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.4.5'] = SRC_URI
        self.defaultTarget = '3.4.5'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['gnuwin32/patch'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, SRC_URI )
        self.instdestdir = "mingw"
        self.subinfo = subinfo()
	
    def unpack( self ):
        base.baseclass.unpack( self )
        srcdir = self.workdir
        cmd = "cd %s && patch -p1 < %s" % \
          ( srcdir, os.path.join( self.packagedir, "vmr9.diff" ) )
        os.system( cmd ) and die( "mingw unpack failed" )
        return True		
    

if __name__ == '__main__':
    subclass().execute()
