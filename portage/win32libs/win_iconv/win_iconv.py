import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/win-iconv/win-iconv.git'
        for ver in ['0.0.4', '0.0.6']:
            self.targets[ver] = 'https://github.com/win-iconv/win-iconv/archive/%s.tar.gz' % ver
            self.archiveNames[ver] = "win-iconv-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'win-iconv-%s' % ver

        self.targetDigests['0.0.6'] = '731bd257920ade27375e3794447d2b291ebfe751'
        self.shortDescription = "a character set conversion library binary compatible with GNU iconv"
        self.defaultTarget = '0.0.6'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

