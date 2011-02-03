import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = '[git]kde:kde-workspace|KDE/4.5|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.5.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.5.' + ver + '/src/kdebase-workspace-4.5.' + ver + '.tar.bz2'
            self.targetInstSrc['4.5.' + ver] = 'kdebase-workspace-4.5.' + ver
        self.targetDigests['4.5.4'] = 'e362bceff622f39bf6949657d1e629ef541c6ae2'
        self.patchToApply['4.5.4'] = [('kdebase-workspace-4.5.4-20101214.diff', 1)]
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde-4.5/kdelibs'] = 'default'
        self.dependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.dependencies['win32libs-bin/freetype'] = 'default'
        self.dependencies['kdesupport/akonadi'] = 'default'
        self.shortDescription = "parts of the KDE desktop"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

