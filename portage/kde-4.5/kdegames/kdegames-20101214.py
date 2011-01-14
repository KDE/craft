import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.5/kdegames'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.5.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.5.' + ver + '/src/kdegames-4.5.' + ver + '.tar.bz2'
            self.targetInstSrc['4.5.' + ver] = 'kdegames-4.5.' + ver
        self.targetDigests['4.5.4'] = '6a0a33d5761c678f37f87a25268e53952134e081'
        self.patchToApply['4.5.4'] = [('kdegames-4.5.4-20101214.diff', 1)]
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.shortDescription = "KDE games applications"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
