import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.shortDescriptions = "audio meta-data library"

    def setTargets( self ):
        for v in ['1.4', '1.5', '1.6', '1.6.1' , '1.6.3','1.7' ]:
          self.targets[ v ] = 'http://developer.kde.org/~wheeler/files/src/taglib-%s.tar.gz' % v
          self.targetInstSrc[ v ] = 'taglib-%s' % v
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        self.patchToApply[ '1.6.3' ] = [("taglib-1.6.3-20101213.diff", 1)]
        self.targetDigests['1.7'] = '5138e1665182bc2171e298ff31518c9ad72ddf23'
        self.shortDescription = "audio metadata library"
        self.defaultTarget = '1.7'

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
