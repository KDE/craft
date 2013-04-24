import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
        self.patchToApply['4.10.0'] = [('kdepim-4.10.0.diff', 1)]
        self.patchToApply['4.10.1'] = [('kdepim-4.10.0.diff', 1)]
        self.patchToApply['4.10.2'] = [('kdepim-4.10.0.diff', 1)]

        self.defaultTarget = 'gitHEAD'

        # Workaround BUG 302342
        self.patchToApply['gitHEAD'] = ('fix_introduction_screen.diff', 1)

    def setDependencies( self ):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.runtimeDependencies['kde/kdepim-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
#        self.dependencies['kdesupport/grantlee'] = 'default'
#        self.dependencies['kde/nepomuk-widgets'] = 'default'
        self.shortDescription = "KDE's Personal Information Management suite"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

        self.subinfo.options.configure.defines = " -DKDEPIM_ONLY_KLEO=True"

if __name__ == '__main__':
    Package().execute()
