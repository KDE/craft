# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '2.3.1', '2.3.2' ]:
          self.targets[ver] = 'http://download.kde.org/download.php?url=stable/amarok/' + ver + '/src/amarok-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'amarok-' + ver

        self.svnTargets['gitHEAD'] = 'git://git.kde.org/amarok.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.dependencies['kdesupport/taglib'] = 'default'
        self.dependencies['kdesupport/taglib-extras'] = 'default'
        self.dependencies['kdesupport/phonon'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['virtual/kdebase-runtime'] = 'default'
        self.dependencies['testing/mysql-pkg'] = 'default'
        self.dependencies['kdesupport/liblastfm'] = 'default'
        self.dependencies['win32libs-bin/gettext'] = 'default'
        self.buildDependencies['testing/qtscriptgenerator'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

