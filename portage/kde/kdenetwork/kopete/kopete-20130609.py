import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
        self.patchToApply['4.10.2'] = [("kopete-kdenetwork-4.8.0-20120125.diff", 1),  # not for upstream, we'll have to find a cleaner solution with the maintainer
                                       ("kopete-mingw-protocols.diff", 1)] # upstreamed

        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs/libidn'] = 'default'
        self.dependencies['win32libs/libmsn'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['win32libs/expat'] = 'default'
        self.dependencies['win32libs/giflib'] = 'default'
        self.dependencies['win32libs/jasper'] = 'default'
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.shortDescription = "a multiprotocol instant messenger"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
