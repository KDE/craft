import base
import utils
import shutil
import os
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/mingw/binutils-2.18.50-20080109-2.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/gcc-4.3.0-20080502-mingw32-alpha-bin.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/mingw32-make-3.81-20080326.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/mingw-runtime-3.14.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/w32api-3.11.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/gdb-6.8-mingw-3.tar.bz2
http://downloads.sourceforge.net/sourceforge/mingw/mingw-utils-0.3.tar.gz
"""

SRC_URI2 = """
http://downloads.sourceforge.net/tdm-gcc/gcc-4.3.2-tdm-2-dw2-core.tar.gz
http://downloads.sourceforge.net/tdm-gcc/gcc-4.3.2-tdm-2-dw2-g%2B%2B.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/binutils-2.18.50-20080109-2.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/mingw32-make-3.81-20080326.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/mingw-runtime-3.14.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/w32api-3.11.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/gdb-6.8-mingw-3.tar.bz2
http://downloads.sourceforge.net/sourceforge/mingw/mingw-utils-0.3.tar.gz
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.3.0'] = SRC_URI
        self.targets['4.3.2-tdm'] = SRC_URI2
        self.defaultTarget = '4.3.0'
    
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
#        cmd = "cd %s && patch -p1 < %s" % \
#          ( srcdir, os.path.join( self.packagedir, "vmr9.diff" ) )
#        self.system( cmd )
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
