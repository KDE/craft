import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.9-2'] = "http://downloads.sourceforge.net/project/kde-windows/kdewin-packager/0.9.9/kdewin-packager-static-vc100-0.9.9-2-bin.tar.bz2"
        self.targetDigests['0.9.9-2'] = '8cc15a649ef33fa24f8ad07be30ef27ab2a6ccbb'
        self.defaultTarget = '0.9.9-2'
    
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True

