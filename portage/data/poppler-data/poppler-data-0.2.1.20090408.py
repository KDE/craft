import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for v in [ '0.2.0', '0.2.1' ]:
          self.targets[v] = 'http://poppler.freedesktop.org/poppler-data-' + v + '.tar.gz'
          self.targetInstSrc[v] = 'poppler-data-' + v
          self.patchToApply[v] = ( 'poppler-data-cmake.patch', 0 )
        self.defaultTarget = '0.2.1'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
