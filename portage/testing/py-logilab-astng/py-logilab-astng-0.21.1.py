
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.21.1'] = 'http://ftp.logilab.org/pub/astng/logilab-astng-0.21.1.tar.gz'
        self.targetInstSrc['0.21.1'] = 'logilab-astng-0.21.1'
        self.targetDigests['0.21.1'] = 'b5c8324e46ab4634f046012a1052c4ad73b1c137'
        self.defaultTarget = '0.21.1'

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.BuildSystemBase import *
from Packager.MultiPackager import *
        
class Package(PackageBase, MultiSource, BuildSystemBase, MultiPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__( self )
        MultiSource.__init__( self )
        BuildSystemBase.__init__( self )
        MultiPackager.__init__( self )
        
    def install( self ): 
        self.system("cd %s && python setup.py install" % self.sourceDir() );
        return True

    def unmerge( self ): 
        print("not supported")
        return False
        
if __name__ == '__main__':
    Package().execute()
