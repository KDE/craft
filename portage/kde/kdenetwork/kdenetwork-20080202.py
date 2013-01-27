import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.9/kdenetwork'
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets['4.9.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.9.' + ver + '/src/kdenetwork-4.9.' + ver + '.tar.xz'
            self.targetInstSrc['4.9.' + ver] = 'kdenetwork-4.9.' + ver
            self.patchToApply['4.9.'+ver] = [("kdenetwork-4.9.0-20120125.diff", 1)]
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs-bin/libidn'] = 'default'
        self.dependencies['win32libs-bin/libmsn'] = 'default'
        self.dependencies['win32libs-bin/mpir'] = 'default'
        self.shortDescription = "KDE Networking applications (Kopete, KGet)"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
