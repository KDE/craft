import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for v in [ '0.2.0', '0.2.1', '0.3.0', '0.4.0', '0.4.1', '0.4.2', '0.4.3', '0.4.4' ]:
          self.targets[v] = 'http://poppler.freedesktop.org/poppler-data-' + v + '.tar.gz'
          self.targetInstSrc[v] = 'poppler-data-' + v
          if v not in ['0.4.2', '0.4.3', '0.4.4']:
            self.patchToApply[v] = ( 'poppler-data-cmake.patch', 0 )
        self.targetDigests['0.4.3'] = 'aa28288563d2542e14414666a8b35d01f42ad164'

        self.svnTargets['gitHEAD'] = "git://git.freedesktop.org/git/poppler/poppler-data"
        self.defaultTarget = '0.4.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.package.withCompiler = False
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
