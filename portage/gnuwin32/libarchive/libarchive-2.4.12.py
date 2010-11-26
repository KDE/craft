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
        self.buildDependencies['virtual/bin-base'] = 'default'
    
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        #self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

        
    def unpack( self ):
        if not BinaryPackageBase.unpack(self):
            return False
        utils.applyPatch( self.sourceDir(), os.path.join( self.packageDir(), "libarchive-comp.diff" ) , "0" )
        return True
 
if __name__ == '__main__':
    Package().execute()
