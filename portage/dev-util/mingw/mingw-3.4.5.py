import base
import utils
import shutil
import os
import info

"""
from trolltech mingw package:

binutils-2.15.91-20040904-1.tar.gz -> 2.19.1
gcc-core-3.4.2-20040916-1.tar.gz -> 3.4.5
gcc-g++-3.4.2-20040916-1.tar.gz -> 3.4.5
mingw32-make-3.80.0-3.exe -> 3.81
mingw-runtime-3.7.tar.gz -> 3.14
w32api-3.2.tar.gz -> 3.11
"""

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/mingw/binutils-2.19.1-mingw32-bin.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/gcc-core-3.4.5-20060117-3.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/gcc-g++-3.4.5-20060117-3.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/mingw32-make-3.81-20080326-3.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/mingw-runtime-3.14.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/w32api-3.11.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/gdb-6.8-mingw-3.tar.bz2
http://downloads.sourceforge.net/sourceforge/mingw/mingw-utils-0.3.tar.gz
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.4.5'] = SRC_URI
        self.defaultTarget = '3.4.5'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['gnuwin32/patch'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, SRC_URI, args=args )
        self.instdestdir = "mingw"
        self.subinfo = subinfo()
	
    def unpack( self ):
        base.baseclass.unpack( self )
        srcdir = self.workdir
        #this patch breaks qt build!
        #cmd = "cd %s && patch -p1 < %s" % \
        #  ( srcdir, os.path.join( self.packagedir, "windef.diff" ) )
        #self.system( cmd )
        #this patch fails
        #cmd = "cd %s && patch -p1 < %s" % \
        #  ( srcdir, os.path.join( self.packagedir, "vmr9.diff" ) )
        #self.system( cmd )
        return True
        
    def install( self ):
        base.baseclass.install( self )
        srcdir = os.path.join( self.imagedir, self.instdestdir, "bin", "mingwm10.dll" )
        destdir = os.path.join( self.imagedir, "bin" )
        if not os.path.exists( destdir ):
            os.mkdir( destdir )
        shutil.copy( srcdir, os.path.join( destdir, "mingwm10.dll" ) )
        return True

if __name__ == '__main__':
    subclass().execute()
