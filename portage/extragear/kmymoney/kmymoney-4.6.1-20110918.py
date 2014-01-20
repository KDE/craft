import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kmymoney'
        for ver in ['4.5.3', '4.6.0', '4.6.1', '4.6.3', '4.6.4']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/kmymoney2/kmymoney-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'kmymoney-' + ver
        self.patchToApply['4.5.3'] = ('kmymoney-4.5.2-20110112.diff', 1)
        self.patchToApply['4.6.0'] = ('kmymoney-4.6.0-20110822.diff', 1)
        self.patchToApply['4.6.1'] = ('kmymoney-4.6.1-20111208.diff', 1)
        self.defaultTarget = '4.6.1'

    def setDependencies( self ):
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['binary/mysql-pkg'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['win32libs/libofx'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.dependencies['extragear/libalkimia'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'
        self.shortDescription = "a personal finance manager for KDE"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False

if __name__ == '__main__':
    Package().execute()
