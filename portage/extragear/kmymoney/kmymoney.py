import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = '[git]kde:kmymoney|master'
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.dependencies['frameworks/kcmutils'] = 'default'
        self.dependencies['frameworks/kdelibs4support'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'
        self.dependencies['testing/gpgmepp'] = 'default'
        self.dependencies['testing/kholidays'] = 'default'
        self.dependencies['binary/mysql-pkg'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        #self.dependencies['win32libs/libofx'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.dependencies['extragear/libalkimia'] = 'default'
        self.dependencies['extragear/kdiagram'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'
        self.shortDescription = "a personal finance manager for KDE"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)

