#import base
import os
import sys
#import info

from Source.ArchiveSource import *
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *
from Packager.KDEWinPackager import *

# deprecated class
class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['default'] = 'http://downloads.sourceforge.net/project/glew/glew/1.5.1/glew-1.5.1-win32.zip'
       
        self.targetMergeSourcePath['default'] = 'glew'
        self.defaultTarget = 'default'
    
class Package(ArchiveSource, BinaryBuildSystem, PackageBase, KDEWinPackager):
    def __init__( self, **args ):
        # we use subinfo for now too 
        self.subinfo = subinfo()
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        PackageBase.__init__(self)
        KDEWinPackager.__init__(self)
        

if __name__ == '__main__':
    Package().execute()
