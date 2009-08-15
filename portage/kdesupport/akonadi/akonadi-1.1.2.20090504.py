# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['win32libs-bin/shared-mime-info'] = 'default'
        self.hardDependencies['win32libs-bin/boost']   = 'default'
        self.hardDependencies['win32libs-bin/libxslt'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.boostversion = "1.37"

    def setTargets( self ):
        self.svnTargets['0.80'] = 'tags/akonadi/0.80'
        self.svnTargets['0.81'] = 'tags/akonadi/0.81'
        self.svnTargets['0.82'] = 'tags/akonadi/0.82'
        self.svnTargets['1.0.0'] = 'tags/akonadi/1.0.0'
        self.svnTargets['1.0.80'] = 'tags/akonadi/1.0.80'
        self.svnTargets['1.1.0']  = 'tags/akonadi/1.1.0'
        self.svnTargets['1.1.1']  = 'tags/akonadi/1.1.1'
        self.svnTargets['1.1.2']  = 'tags/akonadi/1.1.2'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/akonadi'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/akonadi'
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DBoost_ADDITIONAL_VERSIONS=" + self.subinfo.boostversion
        self.boost = portage.getPackageInstance("win32libs-bin","boost")
        self.subinfo.options.configure.defines += " -DBoost_INCLUDE_DIR=" + os.path.join(self.boost.mergeDestinationDir(), "include", "boost-" + self.subinfo.boostversion.replace(".", "_") )

if __name__ == '__main__':
    Package().execute()
