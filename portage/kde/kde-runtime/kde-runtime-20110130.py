import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
        self.patchToApply["4.10.2"] = [("kde-runtime-4.10.2-20130529.diff", 1),#upstream
                                       ("fix-case-sensitivity.diff", 1)]#upstream
        self.patchToApply["4.10.4"] = [("fix-case-sensitivity.diff", 1),#upstream
                                       ("kde-runtime-4.10.4-20130612.diff", 1)]#upstream

        self.shortDescription = 'Components for KDE applications required at runtime'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kde/kactivities'] = 'default'
        self.dependencies['kde/oxygen-icons'] = 'default'
        self.dependencies['win32libs/libssh'] = 'default'
        self.dependencies['kde/kactivities'] = 'default'
        if self.options.features.nepomuk:
            self.dependencies['kde/kdepimlibs'] = 'default'
            self.dependencies['kde/nepomuk-core'] = 'default'
        if compiler.isMinGW_WXX():
            self.dependencies['win32libs/libbfd'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
