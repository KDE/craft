import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/sed-4.1.5-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/sed-4.1.5-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.1.5'] = SRC_URI
        self.targetDigests['4.1.5'] = ['abe52d0be25f1bb44b8a8e7a94e7afa9c15b3ae5',
                                       '736678616305fab80b4ec1a639d5ff0170183310']        
        self.defaultTarget = '4.1.5'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
