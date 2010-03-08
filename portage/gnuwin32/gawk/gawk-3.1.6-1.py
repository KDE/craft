import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/gawk-3.1.6-1-bin.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.1.6-1'] = SRC_URI
        self.defaultTarget = '3.1.6-1'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
