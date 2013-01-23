import utils
import info
from Package.CMakePackageBase import *

# see http://wiki.mozilla.org/LDAP_C_SDK_SASL_Windows

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '2.1.26' ]:
            self.targets[ ver ] = 'ftp://ftp.cyrusimap.org/cyrus-sasl/cyrus-sasl-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'cyrus-sasl-' + ver
        self.patchToApply['2.1.26'] = [( 'cyrus-sasl-2.1.26.patch', 1 )]
        self.shortDescription = "Cyrus SASL implementation"
        self.defaultTarget = '2.1.26'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs/wcecompat'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
#        self.subinfo.options.configure.defines = "-DSTATIC_LIBRARY=OFF"
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
