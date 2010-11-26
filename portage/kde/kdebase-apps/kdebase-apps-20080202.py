import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/apps'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde/kdebase-runtime'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
