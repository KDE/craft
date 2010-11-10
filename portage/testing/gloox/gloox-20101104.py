import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'
        self.hardDependencies['win32libs-bin/libidn'] = 'default'

    def setTargets( self ):
        for ver in ['1.0']:
            self.targets[ ver ] = "http://camaya.net/download/gloox-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "gloox-" + ver
        self.patchToApply['1.0'] = [('gloox-1.0-20101111.diff', 1)]
            
        self.targetDigests['1.0'] = '8c788738f72b05fae7c05c744a67859419ffa09c'

        self.defaultTarget = '1.0'
        self.options.configure.defines = ""

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
