import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['kdesupport/taglib'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib-extras'
        self.targets['1.0.0'] = 'http://kollide.net/~jefferai/taglib-extras-1.0.0.tar.gz'
        self.targetInstSrc['1.0.0'] = 'taglib-extras-1.0.0'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/taglib-extras'
        self.defaultTarget = 'svnHEAD'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
#        self.subinfo.options.configure.defines += "-DWITH_KDE=ON"

if __name__ == '__main__':
    Package().execute()
