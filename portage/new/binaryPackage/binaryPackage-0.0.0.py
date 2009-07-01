#import base
import os
import sys
#import info

from Source.ArchiveSource import *
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *

# deprecated class
class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['default'] = 'http://www.winkde.org/pub/kde/ports/win32/repository/gnuwin32/bzip2-1.0.4-bin.zip'
       
        #self.targetInstSrc['default'] = 'bzip2-1.0.4'
        self.defaultTarget = 'default'
    
    #def setDependencies( self ):
    #    self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
                
class Package(ArchiveSource, BinaryBuildSystem, PackageBase):
    def __init__( self, **args ):
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        PackageBase.__init__(self)
        
        # we use subinfo for now too 
        self.subinfo = subinfo()

if __name__ == '__main__':
    Package().execute()
