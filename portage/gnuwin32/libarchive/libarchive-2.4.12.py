import gnuwin32
import info
import os

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/libarchive-2.4.12-1-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/libarchive-2.4.12-1-lib.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.4.12-1'] = SRC_URI
        self.defaultTarget = '2.4.12-1'

    def setDependencies( self ):
        self.hardDependencies['virtual/win32libs'] = 'default'
        
class subclass(gnuwin32.gnuwin32class):
    def __init__( self, **args ):
        gnuwin32.gnuwin32class.__init__( self, SRC_URI )
        self.subinfo = subinfo()
        
    def compile( self ):
        cmd = "cd %s && patch -p0 < %s" % \
          ( self.workdir, os.path.join( self.packagedir, "libarchive-comp.diff" ) )
        self.system( cmd )
        return True
    
 
if __name__ == '__main__':
    subclass().execute()
