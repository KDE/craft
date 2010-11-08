import info

# sources are in qt.git/util/qlalr, binary is here.
# To build qlalr yourself, go into the Qt sources,
# cd into util/qlalr, and run the following command:
# qmake && nmake
# Additionally, the binary is packaged with upx
# This binary is from the 4.7.0 version of Qt

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['HEAD'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/qlalr.exe"
        self.defaultTarget = 'HEAD'
        ## \todo specific a target independent install path option
        self.targetInstallPath['HEAD'] = 'bin'

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
    def __init__(self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
