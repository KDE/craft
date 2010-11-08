import info
import os

## \todo the dep files will let into have dll's installed multiple times 
SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/grep-%s-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/grep-%s-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        for t in ( '2.5.1a', '2.5.4' ):
          self.targets[ t ] = SRC_URI % ( t, t )
        self.defaultTarget = '2.5.4'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"

        BinaryPackageBase.__init__( self )
        
    def install( self ):
        if not BinaryPackageBase.install( self ):
            return False
        
        manifestDir = os.path.join( self.imageDir(), "manifest"  ) 
        if os.path.exists( manifestDir ):
            for file in os.listdir( manifestDir ):
                if file.endswith( '.mft' ):
                    os.remove( os.path.join( manifestDir, file ) )
        return True

if __name__ == '__main__':
    Package().execute()
