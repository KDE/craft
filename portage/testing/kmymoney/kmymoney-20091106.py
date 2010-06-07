import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdereview/kmymoney'
        self.targets['3.98.1'] = 'http://downloads.sourceforge.net/kmymoney2/kmymoney-3.98.1.tar.bz2'
        self.targetInstSrc['3.98.1'] = 'kmymoney-3.98.1'
        self.patchToApply['3.98.1'] = ('kmymoney-3.98.1.diff', 1)
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['testing/mysql-pkg'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
#        self.softDependencies['testing/libofx'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
    
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
