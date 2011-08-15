import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/office/kmymoney'
        for ver in ['4.5', '4.5.1', '4.5.2', '4.5.3', '4.6.0']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/kmymoney2/kmymoney-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'kmymoney-' + ver
        self.targets['3.98.1'] = 'http://downloads.sourceforge.net/kmymoney2/kmymoney-3.98.1.tar.bz2'
        self.targetInstSrc['3.98.1'] = 'kmymoney-3.98.1'
        self.patchToApply['3.98.1'] = ('kmymoney-3.98.1.diff', 1)
        self.patchToApply['4.5.1'] = ('kmymoney-4.5.1-20101215.diff', 1)
        self.patchToApply['4.5.2'] = ('kmymoney-4.5.2-20110112.diff', 1)
        self.patchToApply['4.5.3'] = ('kmymoney-4.5.2-20110112.diff', 1)
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kdepimlibs'] = 'default'
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['testing/mysql-pkg'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'
        self.dependencies['win32libs-bin/libofx'] = 'default'
        self.dependencies['win32libs-bin/gettext'] = 'default'
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
