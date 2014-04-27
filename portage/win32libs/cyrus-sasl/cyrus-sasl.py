import info
from Package.CMakePackageBase import *

# see http://wiki.mozilla.org/LDAP_C_SDK_SASL_Windows

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '2.1.26' ]:
            self.targets[ ver ] = 'ftp://ftp.cyrusimap.org/cyrus-sasl/cyrus-sasl-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'cyrus-sasl-' + ver
        self.patchToApply['2.1.26'] = [( 'cyrus-sasl-2.1.26.patch', 1 )]
        self.targetDigests['2.1.26'] = 'd6669fb91434192529bd13ee95737a8a5040241c'
        self.shortDescription = "Cyrus SASL implementation"
        self.defaultTarget = '2.1.26'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
#        self.subinfo.options.configure.defines = "-DSTATIC_LIBRARY=OFF"
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
