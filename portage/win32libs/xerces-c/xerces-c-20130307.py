import info

class subinfo( info.infoclass ):

    def setTargets( self ):
        for ver in [ '3.1.2' ]:
            self.targets[ ver ] = 'http://www.apache.org/dist/xerces/c/3/sources/xerces-c-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'xerces-c-' + ver
        self.targetDigests['3.1.2'] = '3f9ecc4956df069c1d95b885fc687eb4e474a4ad'
        self.patchToApply['3.1.2'] = [("xerces-c-3.1.2-20150623.diff", 1)]

        self.shortDescription = "A Validating XML Parser"
        self.defaultTarget = '3.1.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)


if compiler.isMinGW():
    class Package(PackageMSys):
        def __init__( self ):
            PackageMSys.__init__( self )
else:
    class Package(CMakePackageBase):
        def __init__( self ):
            self.subinfo = subinfo()
            CMakePackageBase.__init__( self )

if __name__ == '__main__':
      Package().execute()