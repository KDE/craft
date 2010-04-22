import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for f in ( '16', '17', '18', '18.1', '18.2', '19' ):
          ver = '0.' + f
          self.targets[ver]       = 'http://www.exiv2.org/exiv2-%s.tar.gz' % ver
          self.targetInstSrc[ver] = 'exiv2-%s' % ver
          self.patchToApply[ver]  = ( 'exiv2-%s-cmake.diff' % ver, 0 )

        self.svnTargets['svnHEAD'] = 'svn://dev.robotbattle.com/exiv2/branches/'
        self.defaultTarget = '0.19'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/win_iconv']   = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['win32libs-bin/expat']   = 'default'
        self.hardDependencies['win32libs-bin/zlib']    = 'default'
        self.hardDependencies['virtual/base']          = 'default'
        
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
