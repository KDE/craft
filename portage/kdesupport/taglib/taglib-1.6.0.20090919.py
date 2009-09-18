import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['1.4.0'] = 'http://developer.kde.org/~wheeler/files/src/taglib-1.4.tar.gz'
        self.targetInstSrc['1.4.0'] = 'taglib-1.4'
        self.targets['1.5.0'] = 'http://developer.kde.org/~wheeler/files/src/taglib-1.5.tar.gz'
        self.targetInstSrc['1.5.0'] = 'taglib-1.5'
        self.targets['1.6.0'] = 'http://developer.kde.org/~wheeler/files/src/taglib-1.6.tar.gz'
        self.targetInstSrc['1.6.0'] = 'taglib-1.6'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/taglib'
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
#        self.subinfo.options.configure.defines += " -DBUILD_TESTS=ON"
#        self.subinfo.options.configure.defines += " -DBUILD_EXAMPLES=ON"
#        self.subinfo.options.configure.defines += " -DNO_ITUNES_HACKS=ON"
        self.subinfo.options.configure.defines += " -DWITH_ASF=ON"
        self.subinfo.options.configure.defines += " -DWITH_MP4=ON"

if __name__ == '__main__':
    Package().execute()
