import info


class subinfo(info.infoclass):
    def setDependencies( self ):
    # This Package provides the binaries for uactools-bin but virtual/base can
    # not depend on it because it needs a compiler itself.
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin/tools/mt'
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DCMAKE_EXE_LINKER_FLAGS=-static"

