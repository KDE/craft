import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase/workspace'
        self.svnTargets['4.5'] = 'branches/KDE/4.5/kdebase/workspace'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/workspace'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdebase-workspace-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdebase-workspace-4.0.' + ver
        self.defaultTarget = '4.5'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.5/kdelibs'] = 'default'
        self.hardDependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.hardDependencies['kde-4.5/kdelibs'] = 'default'
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'
        self.hardDependencies['kdesupport/akonadi'] = 'default'
    
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

