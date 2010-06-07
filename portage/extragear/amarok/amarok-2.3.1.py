# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '2.3.1' ] =  'http://download.kde.org/download.php?url=stable/amarok/2.3.1/src/amarok-2.3.1.tar.bz2'
        self.targetInstSrc[ '2.3.1' ] = "amarok-2.3.1"
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/amarok/amarok.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/taglib'] = 'default'
        self.hardDependencies['kdesupport/taglib-extras'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'		
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['testing/mysql-pkg'] = 'default'
       # the following is only a runtime dependency: keep that in mind for later!!!!
        self.hardDependencies['testing/qtscriptgenerator'] = 'default'
        self.compiler=os.getenv('KDECOMPILER')
        if self.compiler != "mingw" and self.compiler != "mingw4":
          self.hardDependencies['testing/liblastfm'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

