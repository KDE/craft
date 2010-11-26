import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/office/kmymoney'
        self.targets['4.5.1'] = 'http://downloads.sourceforge.net/kmymoney2/kmymoney-4.5.1.tar.bz2'
        self.targetInstSrc['4.5.1'] = 'kmymoney-4.5.1'
        self.targets['4.5.0'] = 'http://downloads.sourceforge.net/kmymoney2/kmymoney-4.5.tar.bz2'
        self.targetInstSrc['4.5.0'] = 'kmymoney-4.5'
        self.targets['3.98.1'] = 'http://downloads.sourceforge.net/kmymoney2/kmymoney-3.98.1.tar.bz2'
        self.targetInstSrc['3.98.1'] = 'kmymoney-3.98.1'
        self.patchToApply['3.98.1'] = ('kmymoney-3.98.1.diff', 1)
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['virtual/kdepimlibs'] = 'default'
        self.dependencies['virtual/kdebase-runtime'] = 'default'
        self.dependencies['testing/mysql-pkg'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'
#        self.softDependencies['testing/libofx'] = 'default'
        self.dependencies['win32libs-bin/gettext'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'
    
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
