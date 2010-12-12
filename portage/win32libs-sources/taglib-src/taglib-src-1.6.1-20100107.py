import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        for v in ['1.4', '1.5', '1.6', '1.6.1' , '1.6.3' ]:
          self.targets[ v ] = 'http://developer.kde.org/~wheeler/files/src/taglib-%s.tar.gz' % v
          self.targetInstSrc[ v ] = 'taglib-%s' % v
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/taglib'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.4/taglib'
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
