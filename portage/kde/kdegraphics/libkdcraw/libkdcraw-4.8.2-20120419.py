import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver

        for ver in ['4.10.0', '4.10.1']:
            self.patchToApply[ver] = [('libkdcraw-4.8.0-20120125.diff', 1)]
        for ver in ['4.10.2', '4.10.3']:
            self.patchToApply[ver] = [('libkdcraw-4.10.2-20130420.diff', 1)]

        self.defaultTarget = 'gitHEAD'

        self.shortDescription = 'libkdcraw is a C++ interface around LibRaw library used to decode RAW picture files.'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
