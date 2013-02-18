import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver

        if kd.kdebranch == 'master':
            self.svnTargets['svnHEAD'] = 'trunk/KDE/%s' % self.package
        else:
            self.svnTargets['svnHEAD'] = 'branches/KDE/%s/%s' % (kd.kdeversion[:-1], self.package)

        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs/libidn'] = 'default'
        self.dependencies['win32libs/libmsn'] = 'default'
        self.dependencies['win32libs/mpir'] = 'default'
        self.shortDescription = "KDE Networking applications (Kopete, KGet)"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
