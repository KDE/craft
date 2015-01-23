import info

class subinfo( info.infoclass ):
    def setTargets( self ):

        for ver in ['0.24']:
            self.targets[ver]       = 'http://www.exiv2.org/exiv2-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'exiv2-%s' % ver
        self.targetDigests['0.24'] = '2f19538e54f8c21c180fa96d17677b7cff7dc1bb'
        self.patchToApply['0.24'] = ('exiv2-0.22-20120117.diff', 1)
            
        self.svnTargets['svnHEAD'] = 'svn://dev.exiv2.org/svn/trunk'

        self.shortDescription = "an image metadata library"
        self.defaultTarget = '0.24'

    def setDependencies( self ):
        self.dependencies['win32libs/win_iconv']    = 'default'
        self.dependencies['win32libs/gettext']      = 'default'
        self.dependencies['win32libs/expat']        = 'default'
        self.dependencies['win32libs/zlib']         = 'default'
        self.buildDependencies['virtual/base']      = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.supportsNinja = False#something is wrong with cmake here

