import os
import utils
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.16.0-Beta1'] = 'http://www.libraw.org/data/LibRaw-0.16.0-Beta1.tar.gz'
        self.targetInstSrc['0.16.0-Beta1'] = "LibRaw-0.16.0-Beta1"
        self.targetDigests['0.16.0-Beta1'] = '1bda8b14098b1897264c19728c147bdb43afda60'
        
        self.shortDescription = "LibRaw is a library for reading RAW files obtained from digital photo cameras (CRW/CR2, NEF, RAF, DNG, and others)."
        self.defaultTarget = '0.16.0-Beta1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)
    
if __name__ == '__main__':
    Package().execute()
