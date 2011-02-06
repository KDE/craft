import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.6/kdeplasma-addons'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.6.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.6.' + ver + '/src/kdeplasma-addons-4.6.' + ver + '.tar.bz2'
            self.targetInstSrc['4.6.' + ver] = 'kdeplasma-addons-4.6.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.runtimeDependencies['kde-4.6/kde-runtime'] = 'default'
        self.dependencies['kde-4.6/kdelibs'] = 'default'
        self.dependencies['kde-4.6/kde-workspace'] = 'default'
        self.shortDescription = "several plasma specific addons"

from Package.CMakePackageBase import *
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
