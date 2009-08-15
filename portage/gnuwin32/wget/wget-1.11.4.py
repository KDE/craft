import info

## \todo the dep files will let into have dll's installed multiple times 
SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/wget-%s-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/wget-%s-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        for t in ( '1.10.1', '1.11.4' ):
          self.targets[ t ] = SRC_URI % ( t, t )
        self.defaultTarget = '1.11.4'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
