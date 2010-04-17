import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'

    def setTargets( self ):
        self.svnTargets['2.0.0-5'] = 'tags/qca/2.0.0'
        self.svnTargets['2.0.1-3'] = 'tags/qca/2.0.1'
        self.svnTargets['2.0.2-1'] = 'tags/qca/2.0.2'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qca'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/qca'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.4/kdesupport/qca'
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.onlyBuildTargets = 'umbrello' 
            
if __name__ == '__main__':
    Package().execute()

    
