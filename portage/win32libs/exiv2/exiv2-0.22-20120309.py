import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for f in ( '16', '17', '18', '18.1', '18.2', '19' ):
          ver = '0.' + f
          self.targets[ver]       = 'http://www.exiv2.org/exiv2-%s.tar.gz' % ver
          self.targetInstSrc[ver] = 'exiv2-%s' % ver
          self.patchToApply[ver]  = [( 'exiv2-%s-cmake.diff' % ver, 0 )]
        for f in ( '21', '22' ):
          ver = '0.' + f
          self.targets[ver]       = 'http://www.exiv2.org/exiv2-%s.tar.gz' % ver
          self.targetInstSrc[ver] = 'exiv2-%s' % ver
          self.patchToApply[ver]  = [( 'exiv2-%s-cmake.diff' % ver, 1 )]
        self.patchToApply['0.21'].append(('exiv2-0.21-20101223.diff', 1))
        self.patchToApply['0.22'].append(('exiv2-0.22-20120117.diff', 1))
        # 0.23+ will use svn because cmake support are not included in the tarball but are in the repository
        # exiv2 will eventually fully support cmake
        for f in ( '23' ):
          ver = '0.' + f
          self.svnTargets[ver]       = 'svn://dev.exiv2.org/svn/tags/%s' % ver
        self.svnTargets['svnHEAD'] = 'svn://dev.exiv2.org/svn/trunk'
        self.shortDescription = "an image metadata library"
        self.defaultTarget = '0.22'

    def setDependencies( self ):
        self.dependencies['win32libs/win_iconv']    = 'default'
        self.dependencies['win32libs/gettext']      = 'default'
        self.dependencies['win32libs/expat']        = 'default'
        self.dependencies['win32libs/zlib']         = 'default'
        self.buildDependencies['virtual/base']          = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.supportsNinja = False

if __name__ == '__main__':
    Package().execute()
