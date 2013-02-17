# -*- coding: utf-8 -*-
import info
import utils
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '0.8.2' ]:
            self.targets[ ver ] = 'http://git.kolab.org/libkolabxml/snapshot/libkolabxml-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = "libkolabxml-" + ver
        self.patchToApply['0.8.2'] = [("libkolabxml-fixes.diff", 1)]

        self.shortDescription = ''
        self.defaultTarget = '0.8.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['binary/xsd'] = 'default'

        # the following dependencies are runtime dependencies for packages linking to the static! libkolabxml
        self.dependencies['binary/xerces-c-bin'] = 'default'
        self.dependencies['win32libs/boost-thread'] = 'default'
        self.dependencies['win32libs/boost-system'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_TESTS=OFF"

if __name__ == '__main__':
    Package().execute()
