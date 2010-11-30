import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu/marble'
        self.svnTargets['4.2'] = 'branches/KDE/4.2/kdeedu/marble'
        self.svnTargets['4.3'] = 'branches/KDE/4.3/kdeedu/marble'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['virtual/kdebase-runtime'] = 'default'
    
from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DTILES_AT_COMPILETIME=OFF"

if __name__ == '__main__':
    Package().execute()
