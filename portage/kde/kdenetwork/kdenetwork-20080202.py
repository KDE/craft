import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
        self.patchToApply['4.10.1'] = [("kdenetwork-4.8.0-20120125.diff", 1)]
        self.patchToApply['4.10.2'] = [("kdenetwork-4.10.2-fix-MSVC2010-compile.patch", 1), 
                                       ("kdenetwork-4.10.2-fix-yahoo-mingw.diff", 1), 
                                       ("kdenetwork-4.10.2-fix-jabber-mingw.diff", 1),
                                       ("kdenetwork-krdc-app-icon.diff", 1)]

        if kd.kdebranch == 'master':
            self.svnTargets['svnHEAD'] = 'trunk/KDE/%s' % self.package
        else:
            self.svnTargets['svnHEAD'] = 'branches/KDE/%s/%s' % (kd.kdeversion[:-1], self.package)

        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['extragear/libktorrent'] = 'default'
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
