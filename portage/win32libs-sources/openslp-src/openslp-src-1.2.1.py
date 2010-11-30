# -*- coding: utf-8 -*-
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.2.1'] = "http://mesh.dl.sourceforge.net/sourceforge/openslp/openslp-1.2.1.tar.gz"
        self.targetInstSrc['1.2.1'] = "openslp-1.2.1"
        self.targetDigests['1.2.1'] = '47ab19154084d2b467f09525f5351e9ab7193cf9'
        self.patchToApply['1.2.1'] = [ ("openslp-1.2.1.diff", 0), 
                                       ("openslp-1.2.1-20101130.diff", 1) ]
        self.shortDescription = "openslp daemon and libraries"
        self.defaultTarget = '1.2.1'
    
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
    
from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
