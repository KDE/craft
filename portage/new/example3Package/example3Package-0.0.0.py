# example  
import os
import sys
import info

from Source.MultiSource import *
from BuildSystem.CMakeBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *

# deprecated class
class subinfo(info.infoclass):
    def setTargets( self ):
        print "setTargets"
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin'
        self.targets['archiveHEAD'] = 'http://www.winkde.org/pub/kde/ports/win32/repository-4.3/kdesupport/kdewin-vc90-svnHEAD-src.tar.bz2'
        self.targetInstSrc['archiveHEAD'] = 'src/kdewin-vc90-svnHEAD'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        
                
class Package(PackageBase, MultiSource, CMakeBuildSystem, MultiPackager):
    def __init__( self, **args ):
        # we use subinfo for now too 
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        CMakeBuildSystem.__init__(self)        
        MultiPackager.__init__(self)

if __name__ == '__main__':
    Package().execute()
