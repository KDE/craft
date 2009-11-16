#import base
import os
import sys
#import info

from Package.PackageMultiBase import *

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
        
                
class Package(PackageMultiBase):
    def __init__( self, **args ):
        # we use subinfo for now too 
        self.subinfo = subinfo()
        self.buildSystemType = 'cmake'
        PackageMultiBase.__init__(self)        

if __name__ == '__main__':
    Package().execute()
